from math import log
import pymongo
import utility
from truck import dispatchTruck
from bill import bill
from PyQt5.QtWidgets import QMessageBox


class Consign:
    def __init__(self, SenderName, ReceiverName, SenderPhone, ReceiverPhone, SenderAddress, ReceiverAddress,  volume, branch, SenderMail) -> None:
        self.SenderName = SenderName        # constructor
        self.ReceiverName = ReceiverName
        self.SenderPhone = SenderPhone
        self.ReceiverPhone = ReceiverPhone
        self.SenderAddress = SenderAddress
        self.ReceiverAddress = ReceiverAddress
        self.SenderMail = SenderMail
        self.volume = int(volume)
        self.dateOfArrival = utility.now()
        self.dateOfDispatch = 'NA'
        self.deliveredByTruck = 'NA'
        self.cost = 0
        self.status = 'Unloaded'
        self.branch = branch

    def convertToDictAndUpload(self) -> None:       # convert to dictionary and upload to database
        id = utility.settings.find_one({'_id': 0})['consignID']
        utility.settings.update_one({'_id': 0}, {'$set': {'consignID': id + 1}})
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
            'Destination': utility.closestBranch(self.ReceiverAddress),
            'Status': self.status})


def dispatchConsignment(consignID, truckID) -> None:
    # update dispatch date, delivered by truck, status, At Branch
    # BILL HERE
    # update statistics here
    utility.consignDB.update_one({'_id': consignID}, {'$set': {'Date Of Dispatch': utility.now(), 'Delivered By Truck': truckID, 'At Branch': 'NA', 'Status': 'Dispatched'}})
    consign = utility.consignDB.find_one({'_id': consignID})
    branch = utility.branchDB.find_one({'Location': consign['Destination']})
    oldAvg = branch['Avg. Waiting Time for Consignments']
    oldNo = branch['No. of Consignments Delivered']
    newAvg = (oldAvg * oldNo + utility.deltaTimeToHours(utility.stringToDateTime(utility.now()), utility.stringToDateTime(consign['Date Of Arrival']))) / (oldNo + 1)
    utility.branchDB.update_one({'Location': consign['At Branch']}, {'$set': {'Avg. Waiting Time for Consignments': newAvg, 'No. of Consignments Delivered': oldNo + 1}})
    bill(consign)

def loadConsignment(consignID, truck) -> None:
    # update truck volume, next destination if NA, calculate cost, update branch revenue, consign status, delivered by 
    curVol = truck['Volume Loaded']
    truckID = truck['_id']
    loaded = truck['Consignments Loaded']
    loaded.append(consignID)
    consign = utility.consignDB.find_one({'_id': consignID})
    QMessageBox.information(
        None, "Load Consignment: {}".format(consignID), 
        "Volume: {}\nDestination: {}\nSender's Name: {}\nSender's Address: {}\nReciever's Name: {}, Reciever's Address: {}".format(
        consign['Volume'], consign['Destination'], consign['Sender Name'], consign['Sender Address'], consign['Receiver Name'], consign['Receiver Address']))
    newVol = consign['Volume']
    if truck['Next Destination'] == 'NA':
        truck['Next Destination'] = consign['Destination']
        utility.truckDB.update_one({'_id': truckID}, {'$set': {'Next Destination': truck['Next Destination']}})
    cost = int(100 * newVol * log(200 + utility.distance(consign['At Branch'], truck['Next Destination'])))
    curVol += newVol
    utility.consignDB.update_one({'_id': consignID}, {'$set': {'Status': 'Loaded on truck ' + truck['Number Plate'], 'Delivered By Truck': truckID, 'Cost': cost}})
    utility.branchDB.update_one({'Location': consign['At Branch']}, {'$set': {'Revenue': utility.branchDB.find_one({'Location': consign['At Branch']})['Revenue'] + cost}})
    utility.truckDB.update_one({'_id': truckID}, {'$set': {'Volume Loaded': curVol, 'Consignments Loaded': loaded}})
    if curVol > 500:
        dispatchTruck(truckID)
        return True
    return False