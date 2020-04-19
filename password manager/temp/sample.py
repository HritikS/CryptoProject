import sys
from PyQt4 import QtGui

def window():
   app = QtGui.QApplication(sys.argv)
   w = QtGui.QWidget()
   b = QtGui.QLabel(w)
   b.setText("Hello")
   w.setGeometry(100,100,800,600)
   b.move(50,20)
   w.setWindowTitle("Password Manager ")
   w.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   window()
