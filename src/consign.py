import pymongo
import utility


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
        self.id = None
        self.deliveredByTruck = 'NA'
        self.cost = 0
        self.status = branch

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
            'Status': self.status})