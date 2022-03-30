import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QStackedWidget, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from consign import Consign
from truck import Truck, unloadTruck, changeDriver
from employee import Employee
from utility import checkLogin
import utility
import manager

# login screen
class loginScreen(QDialog):
    def __init__(self):
        super(loginScreen, self).__init__()
        self.setObjectName("Login")
        loadUi('ui/loginscr.ui', self)
        self.loginButton.clicked.connect(self.login)
        self.forgotpasswordButton.clicked.connect(self.forgotpassword)
        self.passwordLineEdit.returnPressed.connect(self.login)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.show()

    def login(self):    # check login credentials
        user = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        self.usernameLineEdit.setText("")
        self.passwordLineEdit.setText("")
        access = checkLogin(user, password)
        self.usernameLineEdit.setFocus()
        if access == True:
            self.accept()
        elif access == False:
            QMessageBox.warning(self, "Log In Error", "Invalid username or password")
        else:
            self.acceptSU()

    def accept(self):   # login as employee
        currentWindow = employeeScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def acceptSU(self):     # login as manager
        currentWindow = managerScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def forgotpassword(self):       # forgot password, it mails the password to the employee's email; in case the mail does not exist but is in the database it will just ignore the error
        res = utility.mailPassword(self.usernameLineEdit.text())
        if res:
            QMessageBox.information(self, "Password Recovery", "Password has been sent to your email")
        else:
            QMessageBox.warning(self, "Password Recovery", "Invalid username")


class employeeScreen(QDialog):      # employee screen
    def __init__(self):
        global widget
        super(employeeScreen, self).__init__()
        self.setObjectName("Employee")
        widget.setWindowTitle("TCC Employee")
        loadUi('ui/employeeHome.ui', self)
        self.employee_name.setText(utility.employeeUser['Name'])
        self.employeeIDLabel.setText(str(utility.employeeUser['_id']))
        self.emailIDLabel.setText(utility.employeeUser['Email'])
        self.branchLabel.setText(utility.employeeUser['Branch'])
        self.backButton.clicked.connect(self.logout)
        self.enterConsignmentButton.clicked.connect(self.enterDetailsPage)
        self.truckUtilButton.clicked.connect(self.truckPage)
        self.show()

    def logout(self):       # logout
        global widget
        widget.setWindowTitle("TCC Log In")
        QMessageBox.warning(self, "Logged Out", "You have logged out.")
        widget.removeWidget(self)

    def enterDetailsPage(self):     # enter consignment details 
        currentWindow = enterConsignDetailsScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def truckPage(self):            # accept trucks and unload them
        currentWindow = truckScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class enterConsignDetailsScreen(QDialog):       # enter consignment details page
    def __init__(self):
        global widget
        widget.setWindowTitle('Register Consignment')
        super(enterConsignDetailsScreen, self).__init__()
        self.setObjectName("Enter Consign Details")
        loadUi('ui/employeeAddConsignment.ui', self)
        self.employee_name.setText(utility.employeeUser['Name'])
        self.employeeIDLabel.setText(str(utility.employeeUser['_id']))
        self.emailIDLabel.setText(utility.employeeUser['Email'])
        self.branchLabel.setText(utility.employeeUser['Branch'])
        self.enterDetailsButton.clicked.connect(self.createConsignment)
        self.backButton.clicked.connect(self.back)
        self.show()

    def back(self):         # back to employee home
        widget.removeWidget(self)

    def createConsignment(self):       # create consignment and add to database
        try:
            a = int(self.volumeLineEdit.text())
        except:
            QMessageBox.warning(self, "Invalid Volume", "Volume must be a number")
            return
        try:
            b = int(self.senderMobileNoLineEdit.text())
            b = int(self.receiverMobileNoLineEdit.text())
        except:
            QMessageBox.warning(self, "Invalid Mobile Number", "Mobile number must be a number")
            return
        if len(self.senderMobileNoLineEdit.text()) != 10 or len(self.receiverMobileNoLineEdit.text()) != 10:
            QMessageBox.warning(self, "Invalid Mobile Number", "Mobile number must be 10 digits")
            return
        createdConsign = Consign(
            self.senderNameLineEdit.text(), 
            self.receiverNameLineEdit.text(), 
            self.senderMobileNoLineEdit.text(), 
            self.receiverMobileNoLineEdit.text(),
            self.senderAddressLineEdit.text(),
            self.receiverAddressLineEdit.text(),
            self.volumeLineEdit.text(),
            utility.employeeUser['Branch'],
            self.senderMailLineEdit.text())
        # if any field is empty discard the operation
        if createdConsign.SenderName == "" or createdConsign.ReceiverName == "" or createdConsign.SenderPhone == "" or createdConsign.ReceiverPhone == "" or createdConsign.SenderAddress == "" or createdConsign.ReceiverAddress == "" or createdConsign.volume == "":
            QMessageBox.warning(self, "Empty Field", "Please fill all the fields")
            return
        self.senderNameLineEdit.setText("") 
        self.receiverNameLineEdit.setText("")
        self.senderMobileNoLineEdit.setText("") 
        self.receiverMobileNoLineEdit.setText("")
        self.senderAddressLineEdit.setText("")
        self.receiverAddressLineEdit.setText("")
        self.volumeLineEdit.setText("")
        self.senderMailLineEdit.setText("")
        createdConsign.convertToDictAndUpload()
        utility.loadUnloadedConsignments(utility.employeeUser['Branch'])


class truckScreen(QDialog):         # truck screen
    def __init__(self):
        global widget
        widget.setWindowTitle('Truck Management')
        super(truckScreen, self).__init__()
        self.setObjectName("Truck")
        loadUi('ui/employeeTruckConfirm.ui', self)
        self.backButton.clicked.connect(self.back)
        self.confirmTruckButton.clicked.connect(self.confirmArrivalOfTruck)
        self.changeDriverButton.clicked.connect(self.changeDriverByPlate)
        trucksHeaded = list(utility.truckDB.find({'Next Destination': utility.employeeUser['Branch']}))
        self.comboBox.clear()
        for t in trucksHeaded:
            self.comboBox.addItem(str(t['Number Plate']))
        self.show()

    def back(self):         # back to employee home
        widget.removeWidget(self)

    def confirmArrivalOfTruck(self):            # confirm arrival of truck
        selectedPlate = self.comboBox.currentText()
        self.comboBox.removeItem(self.comboBox.currentIndex())
        unloadTruck(selectedPlate)
        utility.loadUnloadedConsignments(utility.employeeUser['Branch'])

    def changeDriverByPlate(self):
        try:
            b = int(self.driverNumber.text())
        except:
            QMessageBox.warning(self, "Invalid Mobile Number", "Mobile number must be a number")
            return
        if len(self.driverNumber.text()) != 10:
            QMessageBox.warning(self, "Invalid Mobile Number", "Mobile number must be 10 digits")
            return
        try:            # change driver by truck number plate 
            changeDriver(self.driverName.text(), self.driverNumber.text(), self.numberPlate.text())
            QMessageBox.information(self, "Driver Changed", "Driver changed successfully")   
        except:
            QMessageBox.warning(self, "Invalid Plate", "Invalid plate number")   


class managerScreen(QDialog):
    def __init__(self):         # manager screen
        global widget
        super(managerScreen, self).__init__()
        self.setObjectName("Manager")
        loadUi('ui/managerHome.ui', self)
        widget.setWindowTitle("TCC Manager")
        self.rateLabel.setText("Rate: " + str(utility.Rate))
        self.viewEmployeeButton.clicked.connect(self.goToViewEmployee)
        self.addEmployeeButton.clicked.connect(self.goToAddEmployee)
        self.backButton.clicked.connect(self.goBack)
        self.viewTrucksButton.clicked.connect(self.goToViewTrucks)
        self.addTruckButton.clicked.connect(self.goToAddTruck)
        self.consignmentsButton.clicked.connect(self.goToViewConsignment)
        self.addBranchButton.clicked.connect(self.goToAddBranch)
        self.viewBranchesButton.clicked.connect(self.goToViewBranch)
        self.changeRateButton.clicked.connect(self.changeRateOf)
        self.viewStatButton.clicked.connect(manager.statsPerBranch)
        self.show()

    def goBack(self):           # back to home
        global widget
        widget.setWindowTitle("TCC Log In")
        QMessageBox.warning(self, "Logged Out", "You have logged out.")
        widget.removeWidget(self)

    def goToViewEmployee(self):             # go to view employee
        currentWindow = ViewEmployeeScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToAddEmployee(self):          # go to add employee screen
        currentWindow = AddEmployeeScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToViewTrucks(self):           # go to view trucks screen
        currentWindow = ViewTrucksScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToAddTruck(self):         # go to add truck screen
        currentWindow = AddTruckScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToViewBranch(self):           # go to view branches screen
        currentWindow = ViewBranchScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToAddBranch(self):            # go to add branch screen
        currentWindow = AddBranchScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToViewConsignment(self):          # go to view consignments screen
        currentWindow = ViewConsignmentScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def changeRateOf(self):
        try:
            rate = float(self.rateLineEdit.text())
        except:
            QMessageBox.warning(self, "Invalid Rate", "Rate must be a number")
            return
        if rate < 0:
            QMessageBox.warning(self, "Invalid Rate", "Rate must be positive")
            return
        utility.Rate = rate
        self.rateLineEdit.setText("")
        self.rateLabel.setText("Rate: " + str(utility.Rate))
        QMessageBox.information(self, "Rate Changed", "Rate changed successfully")


class ViewConsignmentScreen(QDialog):           # view consignments screen
    def __init__(self):
        global widget
        widget.setWindowTitle("View Consignment")
        super(ViewConsignmentScreen, self).__init__()
        self.setObjectName("View Consignment")
        loadUi('ui/viewConsignmentutil.ui', self)
        self.searchConsignmentButton.clicked.connect(self.searchConsignment)
        self.backButton.clicked.connect(self.back)
        self.show()

    def searchConsignment(self):            # search consignments function
        res = list(manager.consignmentQuery(self.IDLineEdit.text(), self.senderNameLineEdit.text(), self.receiverNameLineEdit.text()))
        while self.consignmentTable.rowCount() > 0:
            self.consignmentTable.removeRow(0)
        self.consignmentTable.setRowCount(len(res))
        print(len(res))
        for i in range(len(res)):
            self.consignmentTable.setItem(i, 0, QTableWidgetItem(str(res[i]['_id'])))
            self.consignmentTable.setItem(i, 2, QTableWidgetItem(str(res[i]['Sender Name'])))
            self.consignmentTable.setItem(i, 6, QTableWidgetItem(str(res[i]['Receiver Name'])))
            self.consignmentTable.setItem(i, 4, QTableWidgetItem(str(res[i]['Sender Phone'])))
            self.consignmentTable.setItem(i, 8, QTableWidgetItem(str(res[i]['Receiver Phone'])))
            self.consignmentTable.setItem(i, 3, QTableWidgetItem(str(res[i]['Sender Address'])))
            self.consignmentTable.setItem(i, 7, QTableWidgetItem(str(res[i]['Receiver Address'])))
            self.consignmentTable.setItem(i, 1, QTableWidgetItem(str(res[i]['Volume'])))
            self.consignmentTable.setItem(i, 12, QTableWidgetItem(str(res[i]['At Branch'])))
            self.consignmentTable.setItem(i, 5, QTableWidgetItem(str(res[i]['Sender Mail'])))
            self.consignmentTable.setItem(i, 9, QTableWidgetItem(str(res[i]['Date Of Arrival'])))
            self.consignmentTable.setItem(i, 14, QTableWidgetItem(str(res[i]['Status'])))
            self.consignmentTable.setItem(i, 10, QTableWidgetItem(str(res[i]['Date Of Dispatch'])))
            self.consignmentTable.setItem(i, 11, QTableWidgetItem(str(res[i]['Cost'])))
            self.consignmentTable.setItem(i, 13, QTableWidgetItem(str(res[i]['Destination'])))

    def back(self):             # back to manager home
        widget.removeWidget(self)


class ViewEmployeeScreen(QDialog):          # view employee screen
    def __init__(self):
        global widget
        widget.setWindowTitle('Employee Query')
        super(ViewEmployeeScreen, self).__init__()
        self.setObjectName("ViewEmployee")
        loadUi('ui/viewEmployeeUtil.ui', self)
        self.backButton.clicked.connect(self.goBack)
        self.searchButton.clicked.connect(self.query)
        self.fireButton.clicked.connect(self.fireEmployee)
        self.show()

    def goBack(self):               # back to manager home
        widget.removeWidget(self)

    def query(self):                # query employee function
        res = list(manager.employeeQuery(self.IDLineEdit.text(), self.nameLineEdit.text()))
        self.employeeTable.setRowCount(0)
        self.employeeTable.setRowCount(len(res))
        for i in range(len(res)):
            self.employeeTable.setItem(i, 0, QTableWidgetItem(str(res[i]['_id'])))
            self.employeeTable.setItem(i, 1, QTableWidgetItem(str(res[i]['Name'])))
            self.employeeTable.setItem(i, 2, QTableWidgetItem(str(res[i]['Phone'])))
            self.employeeTable.setItem(i, 3, QTableWidgetItem(str(res[i]['Email'])))
            self.employeeTable.setItem(i, 4, QTableWidgetItem(str(res[i]['Address'])))
            self.employeeTable.setItem(i, 5, QTableWidgetItem(str(res[i]['Branch'])))
            self.employeeTable.setItem(i, 6, QTableWidgetItem(str(res[i]['Date Of Joining'])))

    def fireEmployee(self):             # remove employee from database
        try:
            utility.employeeDB.delete_one({"_id": int(self.IDLineEdit.text())})
            QMessageBox.information(self, 'Success', 'Employee Fired')
        except:
            QMessageBox.warning(self, "Error", "Employee not found")



class AddEmployeeScreen(QDialog):               # add employee screen
    def __init__(self):
        global widget
        widget.setWindowTitle('Add Employee')
        super(AddEmployeeScreen, self).__init__()
        self.setObjectName("AddEmployee")
        loadUi('ui/addEmployeeUtil.ui', self)
        self.backButton.clicked.connect(self.goBack)
        self.CreateEmployeeButton.clicked.connect(self.createEmployee)
        self.show()

    def goBack(self):           # back to manager home
        widget.removeWidget(self)

    def createEmployee(self):               # create employee function
        try:
            b = int(self.phoneNumberLineEdit.text())
        except:
            QMessageBox.warning(self, "Invalid Mobile Number", "Mobile number must be a number")
            return
        if len(self.phoneNumberLineEdit.text()) != 10:
            QMessageBox.warning(self, "Invalid Mobile Number", "Mobile number must be 10 digits")
            return
        if utility.branchDB.find_one({"Location":self.branchLocationLineEdit.text()}) is None:
            QMessageBox.warning(self, "Invalid Branch", "Branch does not exist")
            return
        createdEmployee = Employee(
            self.nameLineEdit.text(),
            self.phoneNumberLineEdit.text(),
            self.emailLineEdit.text(),
            self.addressLineEdit.text(),
            self.branchLocationLineEdit.text(),
        )
        # if any of the fields are empty, show error message
        if createdEmployee.name == '' or createdEmployee.phone == '' or createdEmployee.email == '' or createdEmployee.address == '' or createdEmployee.branch == '':
            QMessageBox.warning(self, 'Error', 'Please fill all the fields')
            return
        if utility.employeeDB.find_one({'_id': createdEmployee.email}) is not None:
            QMessageBox.warning(self, 'Error', 'This mail already belongs to an employee. Enter valid details')
            return
        self.nameLineEdit.setText('')
        self.phoneNumberLineEdit.setText('')
        self.emailLineEdit.setText('')
        self.addressLineEdit.setText('')
        self.branchLocationLineEdit.setText('')
        createdEmployee.convertToDictAndUpload()


class ViewTrucksScreen(QDialog):            # view trucks screen
    def __init__(self):
        global widget
        widget.setWindowTitle('View Trucks')
        super(ViewTrucksScreen, self).__init__()
        self.setObjectName("ViewTrucks")
        loadUi('ui/viewTruckUtil.ui', self)
        self.backButton.clicked.connect(self.goBack)
        self.searchButton.clicked.connect(self.query)
        self.historyButton.clicked.connect(self.history)
        self.calcButton.clicked.connect(self.calcIdleTime)
        self.show()

    def goBack(self):           # back to manager home
        widget.removeWidget(self)

    def query(self):            # query trucks function
        res = manager.truckQuery(self.IDLineEdit.text(), self.plateNumberLineEdit.text())
        self.truckTable.setRowCount(1)
        self.truckTable.setItem(0, 0, QTableWidgetItem(str(res['_id'])))
        self.truckTable.setItem(0, 1, QTableWidgetItem(str(res['Time Of Purchase'])))
        self.truckTable.setItem(0, 2, QTableWidgetItem(str(res['Total Consignments Delivered'])))
        self.truckTable.setItem(0, 3, QTableWidgetItem(str(res['Current Driver'])))
        self.truckTable.setItem(0, 4, QTableWidgetItem(str(res['Location'])))
        self.truckTable.setItem(0, 5, QTableWidgetItem(str(res['Number Plate'])))
        self.truckTable.setItem(0, 6, QTableWidgetItem(str(res['Driver Phone'])))
        self.truckTable.setItem(0, 7, QTableWidgetItem(str(res['Status'])))
        self.truckTable.setItem(0, 8, QTableWidgetItem(str(res['Next Destination'])))
        self.truckTable.setItem(0, 9, QTableWidgetItem(str(res['Volume Loaded'])))
        self.truckTable.setItem(0, 10, QTableWidgetItem(str(res['Dispatched At'])))

    def history(self):          # view truck history function
        try:
            history = manager.viewTruckUsageInPeriod(self.IDLineEdit.text(), self.plateNumberLineEdit.text(), self.fromLineEdit.text(), self.toLineEdit.text())
            self.historyTable.setRowCount(0)
            self.historyTable.setRowCount(len(history))
            for i in range(len(history)):
                self.historyTable.setItem(i, 0, QTableWidgetItem(str(history[i]['From'])))
                self.historyTable.setItem(i, 1, QTableWidgetItem(str(history[i]['To'])))
                self.historyTable.setItem(i, 2, QTableWidgetItem(str(history[i]['Dispatched At'])))
                self.historyTable.setItem(i, 3, QTableWidgetItem(str(history[i]['Delivered At'])))
        except:
            QMessageBox.warning(self, 'Error', 'Please enter dates in DD/MM/YYYY format')

    def calcIdleTime(self):             # calculate average idle time function
        try:
            self.idleTimeLineEdit.setText(str(manager.calculateIdleTimeOfTruck(self.IDLineEdit.text(), self.plateNumberLineEdit.text())))
        except:
            QMessageBox.warning(self, 'Error', 'This truck does not exist')


class AddTruckScreen(QDialog):          # add truck screen
    def __init__(self):
        global widget
        widget.setWindowTitle('Add Truck')
        super(AddTruckScreen, self).__init__()
        self.setObjectName("AddTruck")
        loadUi('ui/addTruckUtil.ui', self)
        self.backButton.clicked.connect(self.goBack)
        self.CreateTruckButton.clicked.connect(self.createTruck)
        self.show()

    def goBack(self):           # back to manager home
        widget.removeWidget(self)

    def createTruck(self):          # create truck function
        try:
            b = int(self.driverNumberLineEdit.text())
        except:
            QMessageBox.warning(self, "Invalid Mobile Number", "Mobile number must be a number")
            return
        if len(self.driverNumberLineEdit.text()) != 10:
            QMessageBox.warning(self, "Invalid Mobile Number", "Mobile number must be 10 digits")
            return
        if utility.truckDB.find_one({'Number Plate': self.numberPlateLineEdit.text()}) is not None:
            QMessageBox.warning(self, 'Error', 'This truck already exists')
            return
        if utility.branchDB.find_one({'Location': self.locationLineEdit.text()}) is None:
            QMessageBox.warning(self, 'Error', 'This branch does not exist')
            return
        createdTruck = Truck(
            self.numberPlateLineEdit.text(),
            self.locationLineEdit.text(),
            self.driverNameLineEdit.text(),
            self.driverNumberLineEdit.text(),
        )
        # if any of the fields are empty, show error message
        if createdTruck.numberPlate == '' or createdTruck.CurrentLocation == '' or createdTruck.Driver == '' or createdTruck.driverNumber == '':
            QMessageBox.warning(self, 'Error', 'Please fill all the fields')
            return
        self.numberPlateLineEdit.setText('')
        self.locationLineEdit.setText('')
        self.driverNameLineEdit.setText('')
        self.driverNumberLineEdit.setText('')
        createdTruck.convertToDictAndUpload()
        for b in list(utility.branchDB.find()):
            utility.loadUnloadedConsignments(b['Location'])


class ViewBranchScreen(QDialog):            # view branch screen
    def __init__(self):
        global widget
        widget.setWindowTitle('View Branch')
        super(ViewBranchScreen, self).__init__()
        self.setObjectName("ViewBranch")
        loadUi('ui/viewBranchUtil.ui', self)
        self.backButton.clicked.connect(self.goBack)
        self.searchButton.clicked.connect(self.query)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(4, 300)
        self.table.setColumnWidth(5, 300)
        self.searchConsignmentButton.clicked.connect(self.searchConsignmentsHeaded)
        self.show()

    def goBack(self):               # back to manager home
        widget.removeWidget(self)

    def query(self):            # query branch function
        res = manager.branchQuery(self.locationLineEdit.text())
        if res == None:
            QMessageBox.information(self, "Error", "No Branch Found")
            return
        self.locationLineEdit.setText('')
        self.table.setRowCount(1)
        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem(res['Location']))
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem(res['Address']))
        self.table.setItem(0, 2, QtWidgets.QTableWidgetItem(str(res['Number Of Employees'])))
        self.table.setItem(0, 3, QtWidgets.QTableWidgetItem(str(res['Revenue'])))
        self.table.setItem(0, 4, QtWidgets.QTableWidgetItem(str(res['Average Waiting Time for Consignments'])))
        self.table.setItem(0, 5, QtWidgets.QTableWidgetItem(str(res['Number of Consignments Delivered'])))

    def searchConsignmentsHeaded(self):             # search consignments headed to this branch 
        try:
            cost, res = manager.queryConsignmentsHeadedToSameBranch(self.locationLineEdit.text())
            self.costLineEdit.setText(str(cost))
            while self.consignmentTable.rowCount() > 0:
                self.consignmentTable.removeRow(0)
            self.consignmentTable.setRowCount(len(res))
            for i in range(len(res)):
                self.consignmentTable.setItem(i, 0, QTableWidgetItem(str(res[i]['_id'])))
                self.consignmentTable.setItem(i, 2, QTableWidgetItem(str(res[i]['Sender Name'])))
                self.consignmentTable.setItem(i, 6, QTableWidgetItem(str(res[i]['Receiver Name'])))
                self.consignmentTable.setItem(i, 4, QTableWidgetItem(str(res[i]['Sender Phone'])))
                self.consignmentTable.setItem(i, 8, QTableWidgetItem(str(res[i]['Receiver Phone'])))
                self.consignmentTable.setItem(i, 3, QTableWidgetItem(str(res[i]['Sender Address'])))
                self.consignmentTable.setItem(i, 7, QTableWidgetItem(str(res[i]['Receiver Address'])))
                self.consignmentTable.setItem(i, 1, QTableWidgetItem(str(res[i]['Volume'])))
                self.consignmentTable.setItem(i, 12, QTableWidgetItem(str(res[i]['At Branch'])))
                self.consignmentTable.setItem(i, 5, QTableWidgetItem(str(res[i]['Sender Mail'])))
                self.consignmentTable.setItem(i, 9, QTableWidgetItem(str(res[i]['Date Of Arrival'])))
                self.consignmentTable.setItem(i, 14, QTableWidgetItem(str(res[i]['Status'])))
                self.consignmentTable.setItem(i, 10, QTableWidgetItem(str(res[i]['Date Of Dispatch'])))
                self.consignmentTable.setItem(i, 11, QTableWidgetItem(str(res[i]['Cost'])))
                self.consignmentTable.setItem(i, 13, QTableWidgetItem(str(res[i]['Destination'])))
        except:
            QMessageBox.warning(self, 'Error', 'This branch does not exist')


class AddBranchScreen(QDialog):         # add branch screen
    def __init__(self):
        global widget
        widget.setWindowTitle('Add Branch')
        super(AddBranchScreen, self).__init__()
        self.setObjectName("AddBranch")
        loadUi('ui/addBranchUtil.ui', self)
        self.backButton.clicked.connect(self.goBack)
        self.CreateBranchButton.clicked.connect(self.createBranch)
        self.show()

    def goBack(self):               # back to manager home
        widget.removeWidget(self)

    def createBranch(self):             # create branch function
        createdBranch = utility.Branch(
            self.branchLocationLineEdit.text(),
            self.addressLineEdit.text()
        )
        # if any of the fields are empty, show error message
        if createdBranch.location == '' or createdBranch.address == '':
            QMessageBox.information(self, "Error", "Please fill all the fields")
            return
        if utility.branchDB.find_one({'Location': createdBranch.location}) != None:
            QMessageBox.warning(self, 'Error', 'This branch already exists')
            return
        QMessageBox.information(self, "Success", "Branch Created in {}".format(createdBranch.location))
        self.branchLocationLineEdit.setText('')
        self.addressLineEdit.setText('')
        createdBranch.convertToDictAndUpload()


utility.setupDB()
app = QApplication([])
currentWindow = loginScreen()
widget = QStackedWidget()
widget.setWindowTitle("TCC Log In")
widget.addWidget(currentWindow)
widget.setFixedHeight(840)
widget.setFixedWidth(1351)
widget.show()
sys.exit(app.exec_())