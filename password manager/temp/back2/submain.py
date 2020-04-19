from PyQt4 import QtGui
from PyQt4 import QtCore

import sys, sqlite3, hashlib

class StartWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(StartWindow, self).__init__(parent)
        self.setGeometry(750, 450, 400, 300)
        self.setWindowTitle("Password Manager")
        self.LoginPage()


    def LoginPage(self):
        self.TextPlacer1 = QtGui.QLabel(self)
        self.TextPlacer1.setText("User Name")
        self.TextPlacer1.resize(self.TextPlacer1.sizeHint())
        self.TextPlacer1.move(100, 100)
        self.TextPlacer2 = QtGui.QLabel(self)
        self.TextPlacer2.setText("Password")
        self.TextPlacer2.resize(self.TextPlacer2.sizeHint())
        self.TextPlacer2.move(100, 140)
        self.UserField = QtGui.QLineEdit(self)
        self.UserField.resize(self.UserField.sizeHint())
        self.UserField.move(180, 100)
        self.PassField = QtGui.QLineEdit(self)
        self.PassField.resize(self.PassField.sizeHint())
        self.PassField.move(180, 140)
        self.PassField.setEchoMode(QtGui.QLineEdit.Password)
        self.loginbtn = QtGui.QPushButton("Login", self)
        self.loginbtn.resize(self.loginbtn.sizeHint())
        self.loginbtn.move(180, 170)
        self.CreateNewAcc = QtGui.QPushButton("Create New Account", self)
        self.CreateNewAcc.resize(self.CreateNewAcc.sizeHint())
        self.CreateNewAcc.move(180, 200)
        self.ExitBtn = QtGui.QPushButton("Exit", self)
        self.ExitBtn.resize(self.ExitBtn.sizeHint())
        self.ExitBtn.move(180, 230)
        self.ExitBtn.clicked.connect(self.close_application)
        self.CreateNewAcc.clicked.connect(self.on_pushbutton_clicked)
        self.QDialog = NewApplicationWindow(self)
        self.loginbtn.clicked.connect(self.on_pushbutton_login)
        self.show()

    def close_application(self):
        sys.exit()

    def on_pushbutton_clicked(self):
        self.QDialog.show()

    def on_pushbutton_login(self):
        self.conn = sqlite3.connect('Data.db')
        self.c = self.conn.cursor()
        data = self.c.execute("SELECT * FROM USERS")
        for row in data:
            if row[1] == self.UserField.text() and row[2] == self.PassField.text():
                self.QDialog = Login(self, row[0])
                self.QDialog.show()


class NewApplicationWindow(QtGui.QDialog):
    # NumGridRows = 3
    # NumButtons = 4

    def __init__(self, parent = None):
        super(NewApplicationWindow, self).__init__(parent)
        self.createFormGroupBox()
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accepted)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)
        self.setWindowTitle("Form Layot")

    def createFormGroupBox(self):
        self.formGroupBox = QtGui.QGroupBox("Enter Details")
        layout = QtGui.QFormLayout()
        self.Username = QtGui.QLineEdit()
        self.Password = QtGui.QLineEdit()
        self.Password.setEchoMode(QtGui.QLineEdit.Password)
        layout.addRow(QtGui.QLabel("UserName:"), self.Username)
        layout.addRow(QtGui.QLabel("Password:"), self.Password)
        self.formGroupBox.setLayout(layout)

    def accepted(self):
        self.conn = sqlite3.connect("Data.db")
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO USERS(USERNAME, PASSWORD) VALUES(?, ?)", [(self.Username.text()), (self.Password.text())])
        self.conn.commit()
        print("Successfully Added the account.")
        self.accept()

class Login(QtGui.QMainWindow):
    def __init__(self, parent = None, id = 0):
        super(Login, self).__init__(parent)
        self.setGeometry(650, 450, 800, 600)
        self.setWindowTitle("Password Manager")
        self.profile()

    def profile(self):
        self.Add = QtGui.QPushButton("New", self)
        self.Add.resize(self.Add.sizeHint())
        self.Add.move(100, 200)
        self.Logout = QtGui.QPushButton("Logout", self)
        self.Logout.resize(self.Logout.sizeHint())
        self.Logout.move(100, 300)
        self.Logout.clicked.connect(self.pushLogout)
        self.show()
    def pushLogout(self):
        sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = StartWindow()
    sys.exit(app.exec_())

run()
