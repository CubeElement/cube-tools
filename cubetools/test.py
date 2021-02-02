import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QPushButton, QLineEdit, QListWidget
from PyQt5.QtGui import QFont

class Button(QPushButton):
    def __init__(self, parent):
        super(Button, self).__init__(parent)
        self.setAcceptDrops(True)

        self.setGeometry(QtCore.QRect(90, 90, 61, 51))
        self.setText("Change Me!")
        self.clicked.connect(self.printSomething) #connect here!

    #no need for retranslateUi in your code example

    def printSomething(self):
        print ("Hello")

class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.btn = Button(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.btn)
        self.setLayout(layout)


app = QApplication([])
w = MyWindow()
w.show()
app.exec_()