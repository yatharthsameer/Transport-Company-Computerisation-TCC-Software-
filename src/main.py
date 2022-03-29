from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QStackedWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from consign import Consign
from truck import Truck, unloadTruck
from employee import Employee
from utility import checkLogin
import utility
import manager


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

    def login(self):
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

    def accept(self):
        currentWindow = employeeScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def acceptSU(self):
        currentWindow = managerScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def forgotpassword(self):
        res = utility.mailPassword(self.usernameLineEdit.text())
        if res:
            QMessageBox.information(self, "Password Recovery", "Password has been sent to your email")
        else:
            QMessageBox.warning(self, "Password Recovery", "Invalid username")


class employeeScreen(QDialog):
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

    def logout(self):
        global widget
        widget.setWindowTitle("TCC Log In")
        widget.removeWidget(self)

    def enterDetailsPage(self):
        currentWindow = enterConsignDetailsScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def truckPage(self):
        currentWindow = truckScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class enterConsignDetailsScreen(QDialog):
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
        self.logoutButton.clicked.connect(self.logout)
        self.enterDetailsButton.clicked.connect(self.createConsignment)
        self.backButton.clicked.connect(self.back)
        self.show()

    def logout(self):
        global widget
        widget.setWindowTitle("TCC Log In")
        widget.removeWidget(self)

    def back(self):
        widget.removeWidget(self)

    def createConsignment(self):
        createdConsign = Consign(
            self.senderMailLineEdit.text(), 
            self.receiverNameLineEdit.text(), 
            self.senderMobileNoLineEdit.text(), 
            self.receiverMobileNoLineEdit.text(),
            self.senderAddressLineEdit.text(),
            self.receiverAddressLineEdit.text(),
            self.volumeLineEdit.text(),
            utility.employeeUser['Branch'],
            self.senderMailLineEdit.text())
        self.senderMailLineEdit.setText("") 
        self.receiverNameLineEdit.setText("")
        self.senderMobileNoLineEdit.setText("") 
        self.receiverMobileNoLineEdit.setText("")
        self.senderAddressLineEdit.setText("")
        self.receiverAddressLineEdit.setText("")
        self.volumeLineEdit.setText("")
        self.senderMailLineEdit.setText("")
        createdConsign.convertToDictAndUpload()


class truckScreen(QDialog): ####### WIP
    def __init__(self):
        global widget
        widget.setWindowTitle('Truck Management')
        super(truckScreen, self).__init__()
        self.setObjectName("Truck")
        loadUi('ui/employeeTruckConfirm.ui', self)
        self.backButton.clicked.connect(self.back)
        self.confirmTruckButton.clicked.connect(self.confirmArrivalOfTruck)
        trucksHeaded = utility.truckDB.find({'Next Destination': utility.employeeUser['Branch']})
        self.comboBox.clear()
        for t in trucksHeaded:
            self.comboBox.addItem(str(t['Number Plate']))
        self.show()

    def back(self):
        widget.removeWidget(self)

    def confirmArrivalOfTruck(self):
        selectedPlate = self.comboBox.currentText()
        self.comboBox.removeItem(self.comboBox.currentIndex())
        unloadTruck(selectedPlate)
        


class managerScreen(QDialog):
    def __init__(self):
        global widget
        super(managerScreen, self).__init__()
        self.setObjectName("Manager")
        loadUi('ui/managerHome.ui', self)
        widget.setWindowTitle("TCC Manager")
        self.viewEmployeeButton.clicked.connect(self.goToViewEmployee)
        self.addEmployeeButton.clicked.connect(self.goToAddEmployee)
        self.backButton.clicked.connect(self.goBack)
        self.viewTrucksButton.clicked.connect(self.goToViewTrucks)
        self.addTruckButton.clicked.connect(self.goToAddTruck)
        self.consignmentsButton.clicked.connect(self.goToViewConsignment)
        self.addBranchButton.clicked.connect(self.goToAddBranch)
        self.show()

    def goBack(self):
        global widget
        widget.setWindowTitle("TCC Log In")
        widget.removeWidget(self)

    def goToViewEmployee(self):
        currentWindow = ViewEmployeeScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToAddEmployee(self):
        currentWindow = AddEmployeeScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToViewTrucks(self):
        currentWindow = ViewTrucksScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToAddTruck(self):
        currentWindow = AddTruckScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToAddBranch(self):
        currentWindow = AddBranchScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToViewConsignment(self):
        currentWindow = ViewConsignmentScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ViewConsignmentScreen(QDialog):
    def __init__(self):
        global widget
        widget.setWindowTitle("View Consignment")
        super(ViewConsignmentScreen, self).__init__()
        self.setObjectName("View Consignment")
        loadUi('ui/viewConsignment.ui', self)
        self.searchConsignment.clicked.connect(self.searchConsignment)
        self.backButton.clicked.connect(self.back)
        self.show()

    def searchConsignment(self):
        return manager.consignmentQuery(self.IDLineEdit.text(), self.senderNameLineEdit.text(), self.receiverNameLineEdit.text())

    def back(self):
        widget.removeWidget(self)


class ViewEmployeeScreen(QDialog):
    def __init__(self):
        global widget
        widget.setWindowTitle('Employee Query')
        super(ViewEmployeeScreen, self).__init__()
        self.setObjectName("ViewEmployee")
        loadUi('ui/viewEmployeeUtil.ui', self)
        self.backButton.clicked.connect(self.goBack)
        self.searchButton.clicked.connect(self.query)
        self.show()

    def goBack(self):
        widget.removeWidget(self)

    def query(self):
        manager.employeeQuery(self.IDLineEdit.text(), self.nameLineEdit.text())


class AddEmployeeScreen(QDialog):
    def __init__(self):
        global widget
        widget.setWindowTitle('Add Employee')
        super(AddEmployeeScreen, self).__init__()
        self.setObjectName("AddEmployee")
        loadUi('ui/addEmployeeUtil.ui', self)
        self.backButton.clicked.connect(self.goBack)
        self.CreateEmployeeButton.clicked.connect(self.createEmployee)
        self.show()

    def goBack(self):
        widget.removeWidget(self)

    def createEmployee(self):
        createdEmployee = Employee(
            self.nameLineEdit.text(),
            self.phoneNumberLineEdit.text(),
            self.emailLineEdit.text(),
            self.addressLineEdit.text(),
            self.branchLocationLineEdit.text(),
        )
        self.nameLineEdit.setText('')
        self.phoneNumberLineEdit.setText('')
        self.emailLineEdit.setText('')
        self.addressLineEdit.setText('')
        self.branchLocationLineEdit.setText('')
        createdEmployee.convertToDictAndUpload()


class ViewTrucksScreen(QDialog):
    def __init__(self):
        global widget
        widget.setWindowTitle('View Trucks')
        super(ViewTrucksScreen, self).__init__()
        self.setObjectName("ViewTrucks")
        loadUi('ui/viewTruckUtil.ui', self)
        self.backButton.clicked.connect(self.goBack)
        self.searchButton.clicked.connect(self.query)
        self.show()

    def goBack(self):
        widget.removeWidget(self)

    def query(self):
        manager.truckQuery(self.IDLineEdit.text(), self.plateNumberLineEdit.text())


class AddTruckScreen(QDialog):
    def __init__(self):
        global widget
        widget.setWindowTitle('Add Truck')
        super(AddTruckScreen, self).__init__()
        self.setObjectName("AddTruck")
        loadUi('ui/addTruckUtil.ui', self)
        self.backButton.clicked.connect(self.goBack)
        self.CreateTruckButton.clicked.connect(self.createTruck)
        self.show()

    def goBack(self):
        widget.removeWidget(self)

    def createTruck(self):
        createdTruck = Truck(
            self.numberPlateLineEdit.text(),
            self.locationLineEdit.text(),
            self.driverNameLineEdit.text(),
            self.driverNumberLineEdit.text(),
        )
        self.numberPlateLineEdit.setText('')
        self.locationLineEdit.setText('')
        self.driverNameLineEdit.setText('')
        self.driverNumberLineEdit.setText('')
        createdTruck.convertToDictAndUpload()


class AddBranchScreen(QDialog):
    def __init__(self):
        global widget
        widget.setWindowTitle('Add Branch')
        super(AddBranchScreen, self).__init__()
        self.setObjectName("AddBranch")
        loadUi('ui/addBranchUtil.ui', self)
        self.backButton.clicked.connect(self.goBack)
        self.CreateBranchButton.clicked.connect(self.createBranch)
        self.show()

    def goBack(self):
        widget.removeWidget(self)

    def createBranch(self):
        createdBranch = utility.Branch(
            self.branchLocationLineEdit.text(),
            self.addressLineEdit.text()
        )
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
app.exec_()