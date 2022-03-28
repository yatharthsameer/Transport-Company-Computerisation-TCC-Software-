from math import log
import pymongo
import utility
from truck import dispatchTruck
from bill import bill


class Consign:
    def __init__(self, SenderName, ReceiverName, SenderPhone, ReceiverPhone, SenderAddress, ReceiverAddress,  volume, branch, SenderMail) -> None:
        self.SenderName = SenderName
        self.ReceiverName = ReceiverName
        self.SenderPhone = SenderPhone
        self.ReceiverPhone = ReceiverPhone
        self.SenderAddress = SenderAddress
        self.ReceiverAddress = ReceiverAddress
        self.SenderMail = SenderMail
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
            'Sender Mail' : self.SenderMail,
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
    # update dispatch date, delivered by truck, status, At Branch
    # BILL HERE
    # update statistics here
    utility.consignDB.update_one({'_id': consignID}, {'$set': {'Date Of Dispatch': utility.today(), 'Delivered By Truck': truckID, 'At Branch': 'NA', 'Status': 'Dispatched'}})
    consign = utility.consignDB.find_one({'_id': consignID})
    bill(consign)

def loadConsignment(consignID, truck) -> None:
    # update truck volume, next destination if NA, calculate cost, update branch revenue, consign status, delivered by 
    curVol = truck['Volume Loaded']
    truckID = truck['_id']
    consign = utility.consignDB.find_one({'_id': consignID})
    newVol = consign['Volume']
    if truck['Next Destination'] == 'NA':
        truck['Next Destination'] = utility.closestBranch(consign['Sender Address'])
        utility.truckDB.update_one({'_id': truckID}, {'$set': {'Next Destination': truck['Next Destination']}})
    cost = int(newVol * log(utility.distance(consign['At Branch'], truck['Next Destination'])))
    curVol += newVol
    utility.consignDB.update_one({'_id': consignID}, {'$set': {'Status': 'Loaded on truck ' + truck['Number Plate'], 'Delivered By Truck': truckID, 'Cost': cost}})
    utility.branchDB.update_one({'Location': consign['At Branch']}, {'$set': {'Revenue': utility.branchDB.find_one({'Location': consign['At Branch']})['Revenue'] + cost}})
    utility.truckDB.update_one({'_id': truckID}, {'$set': {'Volume Loaded': curVol}})
    if curVol > 500:
        dispatchTruck(truckID)
        return True
    return False