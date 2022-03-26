import pymongo
import utility


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
            'Next Destination': 'NA'})
        