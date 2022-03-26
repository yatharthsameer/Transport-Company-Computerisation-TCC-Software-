from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QStackedWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from utility import checkLogin
import utility


class loginScreen(QMainWindow):
    def __init__(self):
        super(loginScreen, self).__init__()
        self.setObjectName("Login")
        loadUi('uiOld/loginscr.ui', self)
        self.loginButton.clicked.connect(self.login)
        self.passwordlineEdit.returnPressed.connect(self.login)
        self.passwordlineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.show()

    def login(self):
        access = checkLogin(self.usernamelineEdit.text(), self.passwordlineEdit.text())
        self.usernamelineEdit.setText("")
        self.passwordlineEdit.setText("")
        self.usernamelineEdit.setFocus()
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


class employeeScreen(QMainWindow):
    def __init__(self):
        super(employeeScreen, self).__init__()
        self.setObjectName("Employee")
        loadUi('uiOld/employeescr.ui', self)
        self.logoutButton.clicked.connect(self.goBack)
        self.show()

    def goBack(self):
        currentWindow = loginScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() - 1)


class managerScreen(QMainWindow):
    def __init__(self):
        super(managerScreen, self).__init__()
        self.setObjectName("Manager")
        loadUi('uiOld/managerscr.ui', self)
        self.logoutButton.clicked.connect(self.goBack)
        self.show()

    def goBack(self):
        currentWindow = loginScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() - 1)


utility.setupDB()
app = QApplication([])
currentWindow = loginScreen()
widget = QStackedWidget()
widget.addWidget(currentWindow)
widget.setFixedHeight(861)
widget.setFixedWidth(1351)
widget.show()
app.exec_()