# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_NOTICE_PEER.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Notice_Peer(object):
    def setupUi(self, Notice_Peer):
        Notice_Peer.setObjectName("Notice_Peer")
        Notice_Peer.resize(740, 389)
        self.centralwidget = QtWidgets.QWidget(Notice_Peer)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(80, 50, 651, 251))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -7, 632, 500))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(200, 500))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.R_LISTREGION = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.R_LISTREGION.setGeometry(QtCore.QRect(400, 60, 211, 20))
        self.R_LISTREGION.setObjectName("R_LISTREGION")
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_6.setGeometry(QtCore.QRect(20, 120, 61, 16))
        self.label_6.setObjectName("label_6")
        self.R_OP = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.R_OP.setGeometry(QtCore.QRect(400, 30, 211, 20))
        self.R_OP.setObjectName("R_OP")
        self.O_OP = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.O_OP.setGeometry(QtCore.QRect(100, 30, 211, 20))
        self.O_OP.setObjectName("O_OP")
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_9.setGeometry(QtCore.QRect(20, 160, 71, 16))
        self.label_9.setObjectName("label_9")
        self.label_18 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_18.setGeometry(QtCore.QRect(330, 290, 61, 16))
        self.label_18.setObjectName("label_18")
        self.ELECTING_DATE = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.ELECTING_DATE.setGeometry(QtCore.QRect(100, 160, 201, 20))
        self.ELECTING_DATE.setObjectName("ELECTING_DATE")
        self.label_12 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_12.setGeometry(QtCore.QRect(190, 90, 61, 16))
        self.label_12.setObjectName("label_12")
        self.O_IMSI = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.O_IMSI.setGeometry(QtCore.QRect(100, 260, 211, 20))
        self.O_IMSI.setObjectName("O_IMSI")
        self.O_LISTREGION = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.O_LISTREGION.setGeometry(QtCore.QRect(100, 60, 211, 20))
        self.O_LISTREGION.setObjectName("O_LISTREGION")
        self.label_20 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_20.setGeometry(QtCore.QRect(330, 320, 61, 16))
        self.label_20.setObjectName("label_20")
        self.label_10 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_10.setGeometry(QtCore.QRect(320, 160, 71, 16))
        self.label_10.setObjectName("label_10")
        self.label_17 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_17.setGeometry(QtCore.QRect(40, 320, 61, 16))
        self.label_17.setObjectName("label_17")
        self.SCENARIO = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.SCENARIO.setGeometry(QtCore.QRect(100, 190, 201, 21))
        self.SCENARIO.setObjectName("SCENARIO")
        self.INDEX = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.INDEX.setGeometry(QtCore.QRect(100, 90, 61, 21))
        self.INDEX.setObjectName("INDEX")
        self.label_21 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_21.setGeometry(QtCore.QRect(320, 60, 81, 16))
        self.label_21.setObjectName("label_21")
        self.label_11 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_11.setGeometry(QtCore.QRect(20, 90, 61, 16))
        self.label_11.setObjectName("label_11")
        self.label_14 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_14.setGeometry(QtCore.QRect(320, 30, 61, 16))
        self.label_14.setObjectName("label_14")
        self.R_IMSI = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.R_IMSI.setGeometry(QtCore.QRect(390, 260, 211, 20))
        self.R_IMSI.setObjectName("R_IMSI")
        self.label_16 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_16.setGeometry(QtCore.QRect(40, 260, 61, 16))
        self.label_16.setObjectName("label_16")
        self.label_19 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_19.setGeometry(QtCore.QRect(330, 260, 61, 16))
        self.label_19.setObjectName("label_19")
        self.O_REALM = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.O_REALM.setGeometry(QtCore.QRect(100, 290, 211, 20))
        self.O_REALM.setObjectName("O_REALM")
        self.label_15 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_15.setGeometry(QtCore.QRect(40, 290, 61, 16))
        self.label_15.setObjectName("label_15")
        self.PROCESSED = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.PROCESSED.setGeometry(QtCore.QRect(250, 90, 61, 20))
        self.PROCESSED.setObjectName("PROCESSED")
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_8.setGeometry(QtCore.QRect(320, 190, 61, 16))
        self.label_8.setObjectName("label_8")
        self.UPDATE_DATE = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.UPDATE_DATE.setGeometry(QtCore.QRect(400, 160, 211, 20))
        self.UPDATE_DATE.setObjectName("UPDATE_DATE")
        self.R_REALM = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.R_REALM.setGeometry(QtCore.QRect(390, 290, 211, 20))
        self.R_REALM.setObjectName("R_REALM")
        self.label_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_7.setGeometry(QtCore.QRect(20, 190, 61, 16))
        self.label_7.setObjectName("label_7")
        self.SEND_EMAIL2PEER = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.SEND_EMAIL2PEER.setGeometry(QtCore.QRect(400, 220, 211, 23))
        self.SEND_EMAIL2PEER.setObjectName("SEND_EMAIL2PEER")
        self.label_13 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_13.setGeometry(QtCore.QRect(20, 30, 61, 16))
        self.label_13.setObjectName("label_13")
        self.R_TADIG = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.R_TADIG.setGeometry(QtCore.QRect(390, 320, 211, 20))
        self.R_TADIG.setText("")
        self.R_TADIG.setObjectName("R_TADIG")
        self.POLICY = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.POLICY.setGeometry(QtCore.QRect(400, 190, 211, 20))
        self.POLICY.setObjectName("POLICY")
        self.label_22 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_22.setGeometry(QtCore.QRect(20, 60, 81, 16))
        self.label_22.setObjectName("label_22")
        self.PATH = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.PATH.setGeometry(QtCore.QRect(100, 120, 511, 31))
        self.PATH.setObjectName("PATH")
        self.O_TADIG = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.O_TADIG.setGeometry(QtCore.QRect(100, 320, 211, 20))
        self.O_TADIG.setText("")
        self.O_TADIG.setObjectName("O_TADIG")
        self.InvokeRMT = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.InvokeRMT.setGeometry(QtCore.QRect(320, 90, 101, 17))
        self.InvokeRMT.setObjectName("InvokeRMT")
        self.NEXT_ROUTE = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.NEXT_ROUTE.setGeometry(QtCore.QRect(100, 220, 71, 23))
        self.NEXT_ROUTE.setObjectName("NEXT_ROUTE")
        self.PREVIOUS_ROUTE = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.PREVIOUS_ROUTE.setGeometry(QtCore.QRect(190, 220, 81, 23))
        self.PREVIOUS_ROUTE.setObjectName("PREVIOUS_ROUTE")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        Notice_Peer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Notice_Peer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 740, 21))
        self.menubar.setObjectName("menubar")
        Notice_Peer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Notice_Peer)
        self.statusbar.setObjectName("statusbar")
        Notice_Peer.setStatusBar(self.statusbar)

        self.retranslateUi(Notice_Peer)
        QtCore.QMetaObject.connectSlotsByName(Notice_Peer)

    def retranslateUi(self, Notice_Peer):
        _translate = QtCore.QCoreApplication.translate
        Notice_Peer.setWindowTitle(_translate("Notice_Peer", "MainWindow"))
        self.label_6.setText(_translate("Notice_Peer", "Path"))
        self.label_9.setText(_translate("Notice_Peer", "Electing Date"))
        self.label_18.setText(_translate("Notice_Peer", "R_REALM"))
        self.label_12.setText(_translate("Notice_Peer", "Processed"))
        self.label_20.setText(_translate("Notice_Peer", "R_TADIG"))
        self.label_10.setText(_translate("Notice_Peer", "Update Date"))
        self.label_17.setText(_translate("Notice_Peer", "O_TADIG"))
        self.label_21.setText(_translate("Notice_Peer", "R_LIST_Region"))
        self.label_11.setText(_translate("Notice_Peer", "Index"))
        self.label_14.setText(_translate("Notice_Peer", "R_OP"))
        self.label_16.setText(_translate("Notice_Peer", "O_IMSI"))
        self.label_19.setText(_translate("Notice_Peer", "R_IMSI"))
        self.label_15.setText(_translate("Notice_Peer", "O_REALM"))
        self.label_8.setText(_translate("Notice_Peer", "Policy"))
        self.label_7.setText(_translate("Notice_Peer", "Scenario"))
        self.SEND_EMAIL2PEER.setText(_translate("Notice_Peer", "Send Email to Peer(Upd RMT/Optional)"))
        self.label_13.setText(_translate("Notice_Peer", "O_OP"))
        self.label_22.setText(_translate("Notice_Peer", "O_LIST_Region"))
        self.InvokeRMT.setText(_translate("Notice_Peer", "Invoke RMT"))
        self.NEXT_ROUTE.setText(_translate("Notice_Peer", "Next Route"))
        self.PREVIOUS_ROUTE.setText(_translate("Notice_Peer", "Previous Route"))

