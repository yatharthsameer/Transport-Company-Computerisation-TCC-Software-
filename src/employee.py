import pymongo
import utility
from PyQt5.QtWidgets import QMessageBox


class Employee:
    def __init__(self, name, phone, email, address, branch) -> None:        # constructor
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.branch = branch
        self.dateOfJoining = utility.today()

    def convertToDictAndUpload(self) -> None:                    # convert to dictionary and upload to database
        id = utility.settings.find_one({'_id': 0})['employeeID']
        utility.settings.update_one({'_id': 0}, {'$set': {'employeeID': id + 1}})
        empArr = utility.branchDB.find_one({'Location': self.branch})['Employees']
        empArr.append(id)
        empNo = len(empArr)
        pw = utility.generateRandomString()
        QMessageBox.information(None, "Account Generated", "Check the password in the email sent.")
        utility.sendMail(self.email, False, pw)
        utility.branchDB.update_one({'Location': self.branch}, {'$set': {'Number Of Employees': empNo, 'Employees': empArr}})
        utility.employeeDB.insert_one({
            '_id': id, 
            'Name': self.name, 
            'Phone': self.phone, 
            'Email': self.email, 
            'Address': self.address, 
            'Branch': self.branch, 
            'Date Of Joining': self.dateOfJoining,
            'Password': pw})


def changePassword(employeeMail, newPassword) -> None:          # change password of employee
    utility.employeeDB.update_one({'Email': employeeMail}, {'$set': {'Password': newPassword}})