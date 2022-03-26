import pymongo
import utility


class Consign:
    def __init__(self, name, phone, email, address, branch, dateOfJoining, id) -> None:
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.branch = branch
        self.dateOfJoining = dateOfJoining
        self.id = id

    def convertToDictAndUpload(self) -> None:
        id = utility.settings.find_one({'_id': 0})['ConsignID']
        utility.settings.update_one({'_id': 0}, {'$set': {'ConsignID': id + 1}})
        utility.consignDB.insert_one({'_id': id, 'Name': self.name, 'Phone': self.phone, 'Email': self.email, 'Address': self.address, 'Branch': self.branch, 'Date Of Joining': self.dateOfJoining})