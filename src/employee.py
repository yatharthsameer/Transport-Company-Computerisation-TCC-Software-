import pymongo
import utility


class Employee:
    def __init__(self, name, phone, email, address, branch) -> None:
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.branch = branch
        self.dateOfJoining = utility.today()
        self.id = None

    def convertToDictAndUpload(self) -> None:
        id = utility.settings.find_one({'_id': 0})['EmployeeID']
        utility.settings.update_one({'_id': 0}, {'$set': {'EmployeeID': id + 1}})
        utility.employeeDB.insert_one({
            '_id': id, 
            'Name': self.name, 
            'Phone': self.phone, 
            'Email': self.email, 
            'Address': self.address, 
            'Branch': self.branch, 
            'Date Of Joining': self.dateOfJoining})