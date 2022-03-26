import pymongo
import utility
from truck import dispatchTruck


class Consign:
    def __init__(self, SenderName, ReceiverName, SenderPhone, ReceiverPhone, SenderAddress, ReceiverAddress,  volume, branch) -> None:
        self.SenderName = SenderName
        self.ReceiverName = ReceiverName
        self.SenderPhone = SenderPhone
        self.ReceiverPhone = ReceiverPhone
        self.SenderAddress = SenderAddress
        self.ReceiverAddress = ReceiverAddress
        self.volume = volume
        self.dateOfArrival = utility.today()
        self.dateOfDispatch = 'NA'
        self.deliveredByTruck = 'NA'
        self.cost = 0
        self.status = 'Unloaded'
        self.branch = branch

    def convertToDictAndUpload(self) -> None:
        id = utility.settings.find_one({'_id': 0})['ConsignID']
        utility.settings.update_one({'_id': 0}, {'$set': {'ConsignID': id + 1}})
        utility.consignDB.insert_one({
            '_id': id, 
            'Volume': self.volume,
            'Sender Name': self.SenderName, 
            'Sender Address': self.SenderAddress,
            'Sender Phone': self.SenderPhone, 
            'Receiver Name': self.ReceiverName, 
            'Receiver Address': self.ReceiverAddress, 
            'Receiver Phone': self.ReceiverPhone,
            'Date Of Arrival': self.dateOfArrival,
            'Date Of Dispatch': self.dateOfDispatch,
            'Delivered By Truck': self.deliveredByTruck,
            'Cost': self.cost,
            'At Branch': self.branch,
            'Status': self.status})


def dispatchConsignment(consignID, truckID) -> None:
    utility.consignDB.update_one({'_id': consignID}, {'$set': {'Date Of Dispatch': utility.today(), 'Delivered By Truck': truckID, 'At Branch': 'NA', 'Status': 'Dispatched'}})

def loadConsignment(consignID, truckID) -> None:
    curVol = utility.truckDB.find_one({'_id': truckID})['Volume Loaded']
    if curVol > 500:
        dispatchTruck(truckID)
        return True
    curVol += utility.consignDB.find_one({'_id': consignID})['Volume']
    utility.consignDB.update_one({'_id': consignID}, {'$set': {'Status': 'Loaded', 'Delivered By Truck': truckID}})
    utility.truckDB.update_one({'_id': truckID}, {'$set': {'Volume Loaded': curVol}})
    if curVol > 500:
        dispatchTruck(truckID)
        return True
    return False