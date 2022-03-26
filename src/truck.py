import pymongo
import utility
from consign import dispatchConsignment


class Truck:
    def __init__(self, numberPlate, CurrentLocation, Driver, driverNumber) -> None:
        self.numberPlate = numberPlate
        self.CurrentLocation = CurrentLocation
        self.Driver = Driver
        self.driverNumber = driverNumber
        

    def convertToDictAndUpload(self) -> None:
        id = utility.settings.find_one({'_id': 0})['TruckID']
        utility.settings.update_one({'_id': 0}, {'$set': {'TruckID': id + 1}})
        utility.truckDB.insert_one({
            '_id': id,
            'Last Dispatch Date': 'NA',
            'Total Consignments Delivered': 0,
            'Current Driver': self.Driver, 
            'Location': self.CurrentLocation,
            'Number Plate': self.numberPlate,
            'Driver Phone': self.driverNumber,
            'Consignments Loaded': [],
            'Status': 'Available',
            'Next Destination': 'NA',
            'Volume Loaded': 0})


def changeDriver(newDriverName, newDriverPhone, truckPlateNumber) -> None:
    utility.truckDB.update_one({'Number Plate': truckPlateNumber}, {'$set': {'Current Driver': newDriverName, 'Driver Phone': newDriverPhone}})

def dispatchTruck(truckID) -> None:
    for consignID in utility.truckDB.find_one({'_id': truckID})['Consignments Loaded']:
        dispatchConsignment(consignID, truckID)
    utility.truckDB.update_one({'_id': truckID}, {'$set': {'Status': 'Busy', 'Last Dispatch Date': utility.today()}})

def unloadTruck(truckID) -> None:
    truck = utility.truckDB.find_one({'_id': truckID})
    loc = truck['Next Destination']
    utility.truckDB.update_one({'_id': truckID}, {'$set': {'Status': 'Available', 'Consignments Loaded': [], 'Volume Loaded': 0, 'Next Destination': 'NA', 'Location': loc, 'Total Consignments Delivered': truck['Total Consignments Delivered'] + 1}})