import sys
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog, QApplication, QPushButton, QLineEdit, QFormLayout

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.le = QLineEdit()
        self.le.setObjectName("host")
        self.le.setText("Host")

        self.pb = QPushButton()
        self.pb.setObjectName("connect")
        self.pb.setText("Connect")

        layout = QFormLayout()
        layout.addWidget(self.le)
        layout.addWidget(self.pb)

        self.setLayout(layout)
        self.connect(self.pb, SIGNAL("clicked()"),self.button_click)
        self.setWindowTitle("Learning")

    def button_click(self):
        # shost is a QString object
        shost = self.le.text()
        print(shost)


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
