from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QStackedWidget, QTableWidgetItem
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
        QMessageBox.warning(self, "Logged Out", "You have logged out.")
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
        self.enterDetailsButton.clicked.connect(self.createConsignment)
        self.backButton.clicked.connect(self.back)
        self.show()

    def back(self):
        widget.removeWidget(self)

    def createConsignment(self):
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


class truckScreen(QDialog): ####### WIP
    def __init__(self):
        global widget
        widget.setWindowTitle('Truck Management')
        super(truckScreen, self).__init__()
        self.setObjectName("Truck")
        loadUi('ui/employeeTruckConfirm.ui', self)
        self.backButton.clicked.connect(self.back)
        self.confirmTruckButton.clicked.connect(self.confirmArrivalOfTruck)
        trucksHeaded = list(utility.truckDB.find({'Next Destination': utility.employeeUser['Branch']}))
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
        utility.loadUnloadedConsignments(utility.employeeUser['Branch'])
        


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
        self.viewBranchesButton.clicked.connect(self.goToViewBranch)
        self.show()

    def goBack(self):
        global widget
        widget.setWindowTitle("TCC Log In")
        QMessageBox.warning(self, "Logged Out", "You have logged out.")
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

    def goToViewBranch(self):
        currentWindow = ViewBranchScreen()
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
        loadUi('ui/viewConsignmentutil.ui', self)
        self.searchConsignmentButton.clicked.connect(self.searchConsignment)
        self.backButton.clicked.connect(self.back)
        self.show()

    def searchConsignment(self):
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
        self.historyButton.clicked.connect(self.history)
        self.calcButton.clicked.connect(self.calcIdleTime)
        self.show()

    def goBack(self):
        widget.removeWidget(self)

    def query(self):
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

    def history(self):
        history = manager.viewTruckUsageInPeriod(self.IDLineEdit.text(), self.plateNumberLineEdit.text(), self.fromLineEdit.text(), self.toLineEdit.text())
        self.historyTable.setRowCount(0)
        self.historyTable.setRowCount(len(history))
        for i in range(len(history)):
            self.historyTable.setItem(i, 0, QTableWidgetItem(str(history[i]['From'])))
            self.historyTable.setItem(i, 1, QTableWidgetItem(str(history[i]['To'])))
            self.historyTable.setItem(i, 2, QTableWidgetItem(str(history[i]['Dispatched At'])))
            self.historyTable.setItem(i, 3, QTableWidgetItem(str(history[i]['Delivered At'])))

    def calcIdleTime(self):
        self.idleTimeLineEdit.setText(str(manager.calculateIdleTimeOfTruck(self.IDLineEdit.text(), self.plateNumberLineEdit.text())))


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
        for b in list(utility.branchDB.find()):
            utility.loadUnloadedConsignments(b['Location'])


class ViewBranchScreen(QDialog):
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

    def goBack(self):
        widget.removeWidget(self)

    def query(self):
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
        self.table.setItem(0, 4, QtWidgets.QTableWidgetItem(str(res['Avg. Waiting Time for Consignments'])))
        self.table.setItem(0, 5, QtWidgets.QTableWidgetItem(str(res['No. of Consignments Delivered'])))

    def searchConsignmentsHeaded(self):
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