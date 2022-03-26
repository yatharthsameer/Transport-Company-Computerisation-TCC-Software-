import pymongo
import utility
#hello


class Consign:
    def __init__(self, SenderName, ReceiverName, SenderPhone, ReceiverPhone, SenderAddress, ReceiverAddress,  volume, id) -> None:
        self.SenderName = SenderName
        self.ReceiverName = ReceiverName
        self.SenderPhone = SenderPhone
        self.ReceiverPhone = ReceiverPhone
        self.SenderAddress = SenderAddress
        self.ReceiverAddress = ReceiverAddress
        self.volume = volume
        self.id = id

    def convertToDictAndUpload(self) -> None:
        id = utility.settings.find_one({'_id': 0})['ConsignID']
        utility.settings.update_one({'_id': 0}, {'$set': {'ConsignID': id + 1}})
        utility.consignDB.insert_one({'_id': id, 'SenderName': self.SenderName, 'ReceiverName': self.ReceiverName, 'SenderPhone': self.SenderPhone, 'ReceiverPhone': self.ReceiverPhone, 'SenderAddress': self.SenderAddress, 'ReceiverAddress': self.ReceiverAddress, 'Volume': self.volume})