from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication , QTableWidget , QLineEdit , QLabel , QPushButton , QMessageBox  , QTableWidgetItem , QDialog , QGroupBox , QFormLayout , QDialogButtonBox , QVBoxLayout

from Crypto.Cipher import DES3
from Crypto import Random
from transform import convertpass, convertToMUL8, convertToOriginal
import sys, sqlite3, hashlib

class StartWindow(QMainWindow):
    def __init__(self, parent = None):
        super(StartWindow, self).__init__(parent)
        self.setGeometry(750, 450, 400, 300)
        self.setWindowTitle("Password Manager")
        self.LoginPage()


    def LoginPage(self):
        self.TextPlacer1 = QLabel(self)
        self.TextPlacer1.setText("User Name")
        self.TextPlacer1.resize(self.TextPlacer1.sizeHint())
        self.TextPlacer1.move(100, 100)
        self.TextPlacer2 = QLabel(self)
        self.TextPlacer2.setText("Password")
        self.TextPlacer2.resize(self.TextPlacer2.sizeHint())
        self.TextPlacer2.move(100, 140)
        self.UserField = QLineEdit(self)
        self.UserField.resize(self.UserField.sizeHint())
        self.UserField.move(180, 100)
        self.PassField = QLineEdit(self)
        self.PassField.resize(self.PassField.sizeHint())
        self.PassField.move(180, 140)
        self.PassField.setEchoMode(QLineEdit.Password)
        self.loginbtn = QPushButton("Login", self)
        self.loginbtn.resize(self.loginbtn.sizeHint())
        self.loginbtn.move(180, 170)
        self.CreateNewAcc = QPushButton("Create New Account", self)
        self.CreateNewAcc.resize(self.CreateNewAcc.sizeHint())
        self.CreateNewAcc.move(180, 200)
        self.ExitBtn = QPushButton("Exit", self)
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
        self.m = hashlib.sha512()
        self.m.update(self.PassField.text().encode())
        self.conn = sqlite3.connect('Data.db')
        self.c = self.conn.cursor()
        data = self.c.execute("SELECT * FROM USERS")
        for row in data:
            if row[1] == self.UserField.text() and row[2] == self.m.digest():
                self.QDialog = Login(self, row[0], self.PassField.text())
                self.QDialog.show()


class NewApplicationWindow(QDialog):

    def __init__(self, parent = None):
        super(NewApplicationWindow, self).__init__(parent)
        self.createFormGroupBox()
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accepted)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)
        self.setWindowTitle("Form Layot")

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Enter Details")
        layout = QFormLayout()
        self.Username = QLineEdit()
        self.Password = QLineEdit()
        self.Password.setEchoMode(QLineEdit.Password)
        layout.addRow(QLabel("UserName:"), self.Username)
        layout.addRow(QLabel("Password:"), self.Password)
        self.formGroupBox.setLayout(layout)

    def accepted(self):
        self.m = hashlib.sha512()
        self.m.update(self.Password.text().encode())
        self.conn = sqlite3.connect("Data.db")
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO USERS(USERNAME, PASSWORD) VALUES(?, ?)", [(self.Username.text()), (self.m.digest())])
        self.conn.commit()
        print("Successfully Added the account.")
        self.accept()

class Login(QMainWindow):
    def __init__(self, parent = None, id = 0, passwordString = None):
        super(Login, self).__init__(parent)
        self.passwordStringLocal = passwordString
        self.setGeometry(650, 450, 800, 600)
        self.id = id
        self.setWindowTitle("Password Manager")
        self.conn = sqlite3.connect('Data.db')
        self.c = self.conn.cursor()
        self.profile()

    def profile(self):
        self.Add = QPushButton("New", self)
        self.Add.resize(self.Add.sizeHint())
        self.Add.move(100, 200)
        self.Logout = QPushButton("Logout", self)
        self.Logout.resize(self.Logout.sizeHint())
        self.Logout.move(100, 300)
        self.Logout.clicked.connect(self.pushLogout)
        self.Add.clicked.connect(self.AddIndex)
        self.view = QPushButton("Account List", self)
        self.view.resize(self.view.sizeHint())
        self.view.move(100, 250)
        self.view.clicked.connect(self.AccountList)
        self.show()

    def AccountList(self):
        self.QDialog = passwordList(self, self.id, self.passwordStringLocal)
        # self.QDialog.show()

    def pushLogout(self):
        sys.exit()

    def AddIndex(self):
        self.QDialog = AddPassword(self, self.id, self.passwordStringLocal)
        self.QDialog.show()


class AddPassword(QDialog):
    def __init__(self, parent = None, id = 0, passStringLocalAdd = None):
        super(AddPassword, self).__init__(parent)
        self.id = id
        self.passStringAdd = passStringLocalAdd
        self.createFormGroupBox()
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accepted)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)
        self.setWindowTitle("Add Password")

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("New Account Details")
        layout = QFormLayout()
        self.Username = QLineEdit()
        self.Password = QLineEdit()
        self.Password.setEchoMode(QLineEdit.Password)
        self.Company = QLineEdit()
        layout.addRow(QLabel("UserName/Email"), self.Username)
        layout.addRow(QLabel("Password:"), self.Password)
        layout.addRow(QLabel("Company:"), self.Company)
        self.formGroupBox.setLayout(layout)

    def accepted(self):
        self.conn = sqlite3.connect("Data.db")
        self.c = self.conn.cursor()
        key = convertpass(self.passStringAdd)
        iv = Random.new().read(DES3.block_size)
        cipher_encrypt = DES3.new(key, DES3.MODE_OFB, iv)
        passwordpadded = convertToMUL8(self.Password.text())
        self.c.execute("INSERT INTO PASSES VALUES(?, ?, ?, ?, ?)", [(self.id), (self.Company.text()), (self.Username.text()), (cipher_encrypt.encrypt(convertToMUL8(self.Password.text()))), (iv)])
        print("A New Password FIELD ADDED.")
        self.conn.commit()
        self.accept()


class passwordList(QDialog):
    def __init__(self, parent = None, id = 0, passString = None):
        super(passwordList, self).__init__(parent)
        self.passStringLocal = passString
        self.table = QTableWidget()
        self.tableItem = QTableWidgetItem()
        self.table.setWindowTitle("List of Accounts")
        self.table.resize(800, 600)
        self.table.setColumnWidth(100,100)
        self.conn = sqlite3.connect("Data.db")
        self.c = self.conn.cursor()
        data = self.c.execute("SELECT * FROM PASSES WHERE ID = ?;",[(id)])
        self.counter = 0
        extData = []
        for i in data:
            self.counter += 1
            extData.append(i)
        self.table.setRowCount(self.counter)
        self.table.setColumnCount(3)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setHorizontalHeaderLabels(["Company", "Email/Username", "Password"])
        key = convertpass(self.passStringLocal)
        for i in range(self.counter):
            iv = extData[i][4]
            cipher_decrypt = DES3.new(key, DES3.MODE_OFB, iv)
            self.table.setItem(i, 0, QTableWidgetItem(extData[i][1]))
            self.table.setItem(i, 1, QTableWidgetItem(extData[i][2]))
            self.table.setItem(i, 2, QTableWidgetItem(convertToOriginal(cipher_decrypt.decrypt(extData[i][3]).decode())))
        self.table.show()



def run():
    app = QApplication(sys.argv)
    GUI = StartWindow()
    sys.exit(app.exec_())

run()
