# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/signupDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from ChatRoot import Ui_MainWindow as chatRoot
import time, sys

class Ui_MainWindow(object):
    def __init__(self, client):
        self.Client = client
        self.name, self.surname, self.ID, self.password, self.cit = '', '', '', '', ''
    def loggedOn(self):
        Root_ui = chatRoot(self.Client, self.ID)
        Root_ui.setupUi(self.MainWindow)
        self.MainWindow.show()
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(170, 50, 441, 351))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_4.setInputMask("")
        self.lineEdit_4.setText("")
        #self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_2.addWidget(self.lineEdit_4, 1, 1, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_7.setInputMask("")
        self.lineEdit_7.setText("")
        self.lineEdit_7.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout_2.addWidget(self.lineEdit_7, 4, 1, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_6.setInputMask("")
        self.lineEdit_6.setText("")
        #self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_2.addWidget(self.lineEdit_6, 3, 1, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_5.setInputMask("")
        self.lineEdit_5.setText("")
        #self.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_2.addWidget(self.lineEdit_5, 2, 1, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_2.addWidget(self.lineEdit_3, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(0, 0, 255);")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 5, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.MainWindow = MainWindow
        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(lambda : self.onLogin())
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def onLogin(self):
        self.ID, self.password, self.name, self.surname, self.cit = self.lineEdit_5.text(), self.lineEdit_7.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_6.text()
        #Needed to update information transmission
        try:
            print('I can')
            self.Client.connect()
            self.Client.flush(self.Client.WrappedSock, 'sign up')
            time.sleep(0.5)
            self.Client.flush(self.Client.WrappedSock, self.ID)
            time.sleep(0.5)
            
            self.Client.flush(self.Client.WrappedSock, self.name)
            time.sleep(0.5)
            self.Client.flush(self.Client.WrappedSock, self.surname)
            time.sleep(0.5)
            self.Client.flush(self.Client.WrappedSock, self.ID)
            time.sleep(0.5)
            self.Client.flush(self.Client.WrappedSock, self.cit)
            time.sleep(0.5)
            self.Client.flush(self.Client.WrappedSock, self.password)
            time.sleep(0.5)
            while True:
                if len(self.Client.msg['Server']) == 0:
                    time.sleep(0.5)
                else:
                    if eval(self.Client.msg['Server'].pop()):
                        self.Client.logged = True
                        self.MainWindow.hide()
                        self.loggedOn()
                        break
                    else:
                        break
        except Exception as e:
            print(e)
            self.MainWindow.close()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Mail address:"))
        self.label_5.setText(_translate("MainWindow", "Citizenship"))
        self.label_4.setText(_translate("MainWindow", "Name: "))
        self.label_6.setText(_translate("MainWindow", "Surname:"))
        self.label_7.setText(_translate("MainWindow", "Password:"))
        self.pushButton.setText(_translate("MainWindow", "Complete"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
