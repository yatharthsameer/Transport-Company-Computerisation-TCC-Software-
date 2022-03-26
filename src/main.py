from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QStackedWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from utility import checkLogin
import utility


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
        access = checkLogin(self.usernameLineEdit.text(), self.passwordLineEdit.text())
        self.usernameLineEdit.setText("")
        self.passwordLineEdit.setText("")
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
        super(employeeScreen, self).__init__()
        self.setObjectName("Employee")
        loadUi('ui/employeescr.ui', self)
        self.logoutButton.clicked.connect(self.goBack)
        self.show()

    def goBack(self):
        currentWindow = loginScreen()
        widget.addWidget(currentWindow)
        widget.setCurrentIndex(widget.currentIndex() - 1)


class managerScreen(QDialog):
    def __init__(self):
        super(managerScreen, self).__init__()
        self.setObjectName("Manager")
        loadUi('ui/managerscr.ui', self)
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
widget.setFixedHeight(840)
widget.setFixedWidth(1351)
widget.show()
app.exec_()