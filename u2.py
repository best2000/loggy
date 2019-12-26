# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets, QtWebKi
import pyqtgraph

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(970, 766)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cal1 = QtWidgets.QCalendarWidget(self.centralwidget)
        self.cal1.setGeometry(QtCore.QRect(20, 60, 256, 190))
        self.cal1.setObjectName("cal1")
        self.timeEdit1 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit1.setEnabled(True)
        self.timeEdit1.setGeometry(QtCore.QRect(80, 270, 118, 22))
        self.timeEdit1.setWrapping(False)
        self.timeEdit1.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.timeEdit1.setObjectName("timeEdit1")
        self.timeEdit2 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit2.setEnabled(False)
        self.timeEdit2.setGeometry(QtCore.QRect(350, 270, 118, 22))
        self.timeEdit2.setObjectName("timeEdit2")
        self.cal1_2 = QtWidgets.QCalendarWidget(self.centralwidget)
        self.cal1_2.setEnabled(False)
        self.cal1_2.setGeometry(QtCore.QRect(290, 60, 256, 190))
        self.cal1_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.cal1_2.setObjectName("cal1_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(90, 20, 101, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 47, 14))
        self.label.setObjectName("label")

        self.plot1 = pyqtgraph.PlotWidget(self.centralwidget)
        self.plot1.setGeometry(QtCore.QRect(20, 340, 341, 271))
        self.plot1.addHistogram()

        
        self.plo2 = pyqtgraph.PlotWidget(self.centralwidget)
        self.plo2.setGeometry(QtCore.QRect(370, 340, 341, 271))
        self.plo2.setObjectName("plo2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 970, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.timeEdit1.setDisplayFormat(_translate("MainWindow", "hh:mm:ss"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Date"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Date-Date"))
        self.label.setText(_translate("MainWindow", "Filter by"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
