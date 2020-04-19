import sys
from PyQt4 import QtGui
import sqlite3
import hashlib


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle("Password Manager")
        self.setWindowIcon(QtGui.QIcon('programlogo.png'))
        self.conn = sqlite3.connect('Data.db')
        self.c = self.conn.cursor()
        self.home()

    def home(self):
        self.textPlacer = QtGui.QLabel(self)
        self.textPlacer.setText("UserName")
        self.textPlacer.resize(self.textPlacer.sizeHint())
        self.textPlacer.move(225, 205)
        self.textPlacer2 = QtGui.QLabel(self)
        self.textPlacer2.setText("Password")
        self.textPlacer2.resize(self.textPlacer2.sizeHint())
        self.textPlacer2.move(225, 235)
        self.password = QtGui.QLineEdit(self)
        self.password.move(300, 230)
        self.password.resize(self.password.sizeHint())
        # self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.username = QtGui.QLineEdit(self)
        self.username.move(300, 200)
        # self.username.setPlaceholderText("Enter User Name")
        self.username.resize(self.username.sizeHint())
        self.loginBtn = QtGui.QPushButton("Login", self)
        self.loginBtn.clicked.connect(self.login)
        self.loginBtn.resize(self.loginBtn.sizeHint())
        self.loginBtn.move(285, 260)
        self.exitBtn = QtGui.QPushButton("Quit", self)
        self.exitBtn.clicked.connect(self.close_application)
        self.exitBtn.resize(self.exitBtn.sizeHint())
        self.exitBtn.move(385, 260)
        self.show()

    def CreateAccount(self):
        pass



    def login(self):
        print("username {}".format(self.username.text()))
        print("password {}".format(self.password.text()))
        self.c.execute("INSERT INTO pass values(?, ?);", [(self.username.text()), (self.password.text())])
        self.conn.commit()


    def close_application(self):
        print("Program Closed")
        sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
