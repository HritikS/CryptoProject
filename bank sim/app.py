import sys
from PyQt4 import QtGui
import sqlite3
import hashlib
import seccure


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Bank Simulation")
        self.resize(400, 300)
        self.move(700, 400)
        self.Controls()
        self.show()

    def Controls(self):
        self.UserName = QtGui.QLineEdit(self)
        self.Password = QtGui.QLineEdit(self)
        self.Password.setEchoMode(QtGui.QLineEdit.Password)
        self.UserName.move(180, 100)
        self.Password.move(180, 150)
        self.TextUser = QtGui.QLabel("UserName: ", self)
        self.TextPass = QtGui.QLabel("Password: ", self)
        self.TextUser.move(100, 100)
        self.TextPass.move(100, 150)
        self.ExitButton = QtGui.QPushButton("Exit", self)
        self.ExitButton.move(150, 250)
        self.ExitButton.clicked.connect(self.on_click_exit)
        self.LoginButton = QtGui.QPushButton("Login", self)
        self.LoginButton.move(200, 200)
        self.LoginButton.clicked.connect(self.on_click_login)
        self.SignUpButton = QtGui.QPushButton("Sign Up", self)
        self.SignUpButton.move(100, 200)
        self.SignUpButton.clicked.connect(self.on_click_signup)

    def on_click_signup(self):
        self.SignUp = SignUpWindow()

    def on_click_exit(self):
        sys.exit()

    def on_click_login(self):
        self.conn = sqlite3.connect("BankDB.db")
        self.c = self.conn.cursor()
        self.h = hashlib.sha512()
        self.h.update(self.Password.text().encode())
        self.hash = self.h.digest()
        for i in self.c.execute("SELECT * FROM USERS;"):
            if i[1] == self.UserName.text() and i[2] == self.hash:
                self.Login = LoginedScreen(i[3])
                self.close()
class LoginedScreen(QtGui.QMainWindow):
    def __init__(self, accID):
        super(LoginedScreen, self).__init__()
        self.accID = accID
        self.resize(400, 400)
        self.move(600, 250)
        self.setWindowTitle("Welcome {}".format('USER'))
        self.ButtonTL = QtGui.QPushButton("Transaction Log", self)
        self.ButtonTL.clicked.connect(self.on_click_TL)
        self.ButtonTL.resize(self.ButtonTL.sizeHint())
        self.ButtonTF = QtGui.QPushButton("Transfer Funds", self)
        self.ButtonTF.move(100, 300)
        self.ButtonTL.move(100, 200)
        self.ButtonTF.resize(self.ButtonTF.sizeHint())
        self.ButtonTF.clicked.connect(self.on_click_TF)
        self.ButtonExit = QtGui.QPushButton("Login Out", self)
        self.ButtonExit.resize(self.ButtonExit.sizeHint())
        self.ButtonExit.move(100, 350)
        self.ButtonExit.clicked.connect(self.on_click_exit)
        self.TotalBalance = QtGui.QPushButton("Net Balance", self)
        self.TotalBalance.resize(self.TotalBalance.sizeHint())
        self.TotalBalance.move(100, 150)
        self.TotalBalance.clicked.connect(self.on_click_net_balance)
        self.show()

    def on_click_net_balance(self):
        self.NetBalanceScreen = NetBalanceScreen(self.accID)

    def on_click_exit(self):
        sys.exit()

    def on_click_TF(self):
        self.TF = TransferFundsWindow(self.accID)
    def on_click_TL(self):
        self.TL = Transaction_log(self.accID)

class TransferFundsWindow(QtGui.QMainWindow):
    def __init__(self, accID):
        super(TransferFundsWindow, self).__init__()
        self.resize(400, 400)
        self.accID = accID
        self.move(700, 400)
        self.LabelSendTo = QtGui.QLabel("Send To:", self)
        self.LabelAmount = QtGui.QLabel("Amount:", self)
        self.LabelSendTo.move(145, 100)
        self.LabelAmount.move(145, 200)
        self.ReceiversID = QtGui.QLineEdit(self)
        self.Amount = QtGui.QLineEdit(self)
        self.ReceiversID.move(200, 100)
        self.Amount.move(200, 200)
        self.ButtonSend = QtGui.QPushButton("Send", self)
        self.BUttonCancel = QtGui.QPushButton("Cancel", self)
        self.ButtonSend.move(100, 300)
        self.BUttonCancel.move(200, 300)
        self.BUttonCancel.clicked.connect(self.on_click_cancel)
        self.ButtonSend.clicked.connect(self.on_click_send)
        self.show()

    def on_click_send(self):
        self.conn = sqlite3.connect('BankDB.db')
        self.c = self.conn.cursor()
        self.c.execute('INSERT INTO SAMPE VALUES(?, ?, ?, ?, ?, ?, ?);', [(self.accID), (self.accID), (self.ReceiversID.text()), (self.Amount.text()) , ('sometime'), ('also sometime'), ('hashvalue of some time')])
        print("Successfully Transfered")
        # self.fetchdata = self.c.execute('SELECT NETBALANCE FROM USERS where ACCOUNT_ID = ?', [(self.accID)])
        # for i in self.fetchdata:
        #     self.intbalnow = i[0]
        # self.c.execute('UPDATE USERS SET NETBALANCE = ? WHERE ACCOUNT_ID = ?',[(self.intbalnow - int(self.Amount.text())), (self.accID)])
        self.conn.commit()
        self.close()

    def on_click_cancel(self):
        self.close()




class Transaction_log(QtGui.QTableWidget):
    def __init__(self, accID):
        super(Transaction_log, self).__init__()
        self.accID = accID
        self.setWindowTitle("Welcome User")
        self.resize(1200, 600)
        self.tableItem = QtGui.QTableWidgetItem()
        self.setRowCount(4)
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(('Sender', 'Receiver', 'Transaction Amount', 'Date of Transaction', 'Time of Transaction', 'Transaction ID'))
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 200)
        self.setColumnWidth(3, 200)
        self.setColumnWidth(4, 200)
        self.setColumnWidth(5, 200)
        self.fetch()
        self.show()

    def fetch(self):
        self.conn = sqlite3.connect('BankDB.db')
        self.c = self.conn.cursor()
        self.data = self.c.execute('SELECT SENDER_ID, RECEIVER_ID, TRANSACTION_AMOUNT, DOT, TOT, TRANSACTION_ID from SAMPE where ACCOUNT_ID = ? or RECEIVER_ID = ?', [(self.accID), (self.accID)])
        j = 0
        for i in self.data:
            self.setItem(j, 0, QtGui.QTableWidgetItem(str(i[0])))
            self.setItem(j, 1, QtGui.QTableWidgetItem(str(i[1])))
            self.setItem(j, 2, QtGui.QTableWidgetItem(str(i[2])))
            self.setItem(j, 3, QtGui.QTableWidgetItem(str(i[3])))
            self.setItem(j, 4, QtGui.QTableWidgetItem(str(i[4])))
            self.setItem(j, 5, QtGui.QTableWidgetItem(str(i[5])))
            j += 1


class SignUpWindow(QtGui.QMainWindow):
    def __init__(self):
        super(SignUpWindow, self).__init__()
        self.setWindowTitle("Sign Up Window")
        self.resize(500, 500)
        self.Control()
        self.show()

    def Control(self):
        self.TextName = QtGui.QLabel("Name:", self)
        self.TextName.move(200, 50)
        self.TextUserName = QtGui.QLabel("User Name:", self)
        self.TextUserName.move(170, 100)
        self.TextPassword = QtGui.QLabel("Password:", self)
        self.TextPassword.move(180, 150)
        self.TextAccountNumber = QtGui.QLabel("Account Number:", self)
        self.TextAccountNumber.move(130, 200)
        self.TextAccountNumber.resize(self.TextAccountNumber.sizeHint())
        self.TextNetBalance = QtGui.QLabel("Net Balance:", self)
        self.TextNetBalance.move(160, 250)
        self.NameField = QtGui.QLineEdit(self)
        self.NameField.move(250, 50)
        self.User_NameField = QtGui.QLineEdit(self)
        self.User_NameField.move(250, 100)
        self.PasswordField = QtGui.QLineEdit(self)
        self.PasswordField.setEchoMode(QtGui.QLineEdit.Password)
        self.PasswordField.move(250, 150)
        self.Account_NumberField = QtGui.QLineEdit(self)
        self.Account_NumberField.move(250, 200)
        self.NetBalance = QtGui.QLineEdit(self)
        self.NetBalance.move(250, 250)
        self.SubmitButton = QtGui.QPushButton("Submit", self)
        self.SubmitButton.move(280, 400)
        self.CancelButton = QtGui.QPushButton("Cancel", self)
        self.CancelButton.move(180, 400)
        self.SubmitButton.clicked.connect(self.on_click_submit)
        self.CancelButton.clicked.connect(self.on_click_cancel)

    def on_click_submit(self):
        self.conn = sqlite3.connect("BankDB.db")
        self.c = self.conn.cursor()
        self.h = hashlib.sha512()
        self.h.update(self.PasswordField.text().encode())
        self.hash = self.h.digest()
        self.c.execute("INSERT INTO USERS(NAME, USERNAME, PASSWORD, ACCOUNT_ID) VALUES(?, ?, ?, ?)", [(self.NameField.text()), (self.User_NameField.text()), (self.hash), (self.Account_NumberField.text())])
        self.c.execute('INSERT INTO SAMPE VALUES(00001, 00001, ?, ?, ?, ?, ?)', [(self.Account_NumberField.text()), (self.NetBalance.text()), ('some time'), ('Some TOT'), ('TR')])
        self.conn.commit()
        self.conn.close()
        self.close()

    def on_click_cancel(self):
        self.result = QtGui.QMessageBox.question(self, 'Alert', "Do you want to leave this page ?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if self.result == QtGui.QMessageBox.Yes:
            self.close()

class NetBalanceScreen(QtGui.QMainWindow):
    def __init__(self, accID):
        super(NetBalanceScreen, self).__init__()
        self.resize(200, 200)
        self.accID = accID
        self.CalBAL()
        self.Label = QtGui.QLabel("Net Balance", self)
        self.Balance = QtGui.QLineEdit(self)
        self.Balance.setText(str(self.NETBAL))
        self.Balance.setReadOnly(True)
        self.Label.move(50, 50)
        self.Balance.move(50, 100)
        self.show()

    def CalBAL(self):
        self.conn = sqlite3.connect('BankDB.db')
        self.c = self.conn.cursor()
        self.data = self.c.execute('SELECT TRANSACTION_AMOUNT FROM SAMPE WHERE RECEIVER_ID = ?;', [(self.accID)])
        self.pos = 0
        for i in self.data:
            self.pos += int(i[0])
        self.data = self.c.execute('SELECT TRANSACTION_AMOUNT FROM SAMPE WHERE SENDER_ID = ?;', [(self.accID)])
        self.neg = 0
        for i in self.data:
            self.neg += int(i[0])
        # self.bald = self.c.execute('SELECT NETBALANCE FROM USERS WHERE ACCOUNT_ID = ?;',[(self.accID)])
        print(self.accID)
        self.NETBAL = self.pos - self.neg

if __name__ == "__main__":
    App = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(App.exec_())
