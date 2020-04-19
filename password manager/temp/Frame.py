import sys
from PyQt4 import QtGui, QtCore

class window(QtGui.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle("Password Manager")
        self.setWindowIcon(QtGui.QIcon('programlogo.png'))

        extractAction = QtGui.QAction("&LEAVE THE APPLICATION", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip("Leave the app")
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        self.le = QtGui.QLineEdit()
        self.le.setObjectName("host")
        self.le.setText("Host")
        layout = QtGui.QFormLayout()
        layout.addWidget(self.le)
        self.setLayout(layout)

        self.home()

    def home(self):
        userName = QtGui.QLineEdit()
        userName.setReadOnly(True)
        btn = QtGui.QPushButton("Quit", self)
        btn_login = QtGui.QPushButton("Login In", self)
        # btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.clicked.connect(self.close_application)
        btn_login.clicked.connect(self.login_in)
        btn_login.move(100, 200)
        btn.resize(btn.sizeHint())
        btn.move(400, 500)
        self.show()

    def login_in(self):
        print(userName)


    def close_application(self):
        print('Program Closed')
        sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = window()
    sys.exit(app.exec_())

run()
