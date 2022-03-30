import pymongo
import utility
import consign
from PyQt5.QtWidgets import QMessageBox


class Truck:
    def __init__(self, numberPlate, CurrentLocation, Driver, driverNumber) -> None:         # constructor
        self.numberPlate = numberPlate
        self.CurrentLocation = CurrentLocation
        self.Driver = Driver
        self.driverNumber = driverNumber
        

    def convertToDictAndUpload(self) -> None:           # convert to dictionary and upload to database
        id = utility.settings.find_one({'_id': 0})['truckID']
        utility.settings.update_one({'_id': 0}, {'$set': {'truckID': id + 1}})
        utility.truckDB.insert_one({
            '_id': id,
            'Time Of Purchase' : utility.now(),
            'Total Consignments Delivered': 0,
            'Current Driver': self.Driver, 
            'Location': self.CurrentLocation,
            'Number Plate': self.numberPlate,
            'Driver Phone': self.driverNumber,
            'Consignments Loaded': [],
            'Status': 'Available',
            'Next Destination': 'NA',
            'Volume Loaded': 0,
            'Delivery History': [],
            'Dispatched At': 'NA'})


def changeDriver(newDriverName, newDriverPhone, truckPlateNumber) -> None:              # change driver of truck
    utility.truckDB.update_one({'Number Plate': truckPlateNumber}, {'$set': {'Current Driver': newDriverName, 'Driver Phone': newDriverPhone}})

def dispatchTruck(truckID) -> None:                                        # dispatch truck
    for consignID in utility.truckDB.find_one({'_id': truckID})['Consignments Loaded']:
        consign.dispatchConsignment(consignID, truckID)         # dispatch consignments loaded inside
    utility.truckDB.update_one({'_id': truckID}, {'$set': {'Status': 'Enroute', 'Dispatched At': utility.now()}})

def unloadTruck(truckPlate) -> None:                              # unload truck and update statistics and history
    QMessageBox.information(None, 'Incoming Truck', 'Truck {} Unloaded'.format(truckPlate))
    truck = utility.truckDB.find_one({'Number Plate': truckPlate})
    num = len(truck['Consignments Loaded'])
    loc = truck['Next Destination']
    prevLoc = truck['Location']
    History = truck['Delivery History']
    History.append({'From': prevLoc, 'To': loc, 'Dispatched At': truck['Dispatched At'], 'Delivered At': utility.now()})
    for consign in truck['Consignments Loaded']:
        utility.consignDB.update_one({'_id': consign}, {'$set': {'Status': 'Delivered'}})
    utility.truckDB.update_one({'Number Plate': truckPlate}, {'$set': {
        'Status': 'Available', 
        'Consignments Loaded': [], 
        'Volume Loaded': 0, 
        'Next Destination': 'NA', 
        'Location': loc, 
        'Total Consignments Delivered': truck['Total Consignments Delivered'] + num, 
        'Delivery History': History, 
        'Dispatched At': 'NA'}})