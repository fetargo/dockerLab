from functools import update_wrapper
from sys import path
from PyQt5 import QtCore, QtGui, QtWidgets
import Client
from PIL import Image

class Ui_MainWindow(object):
    errorCode = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(802, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 801, 551))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tcpButton = QtWidgets.QPushButton(self.tab)
        self.tcpButton.setGeometry(QtCore.QRect(0, 480, 791, 41))
        self.tcpButton.setObjectName("tcpButton")
        self.tcpGroupBox = QtWidgets.QGroupBox(self.tab)
        self.tcpGroupBox.setGeometry(QtCore.QRect(240, 0, 551, 471))
        self.tcpGroupBox.setTitle("")
        self.tcpGroupBox.setObjectName("tcpGroupBox")
        self.labelFoto = QtWidgets.QLabel(self.tcpGroupBox)
        self.labelFoto.setGeometry(QtCore.QRect(20, 30, 521, 431))
        self.labelFoto.setText("")
        self.labelFoto.setObjectName("labelFoto")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(10, 10, 111, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 221, 401))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.tcpStatusLabel = QtWidgets.QLabel(self.tab)
        self.tcpStatusLabel.setGeometry(QtCore.QRect(10, 30, 221, 21))
        self.tcpStatusLabel.setObjectName("tcpStatusLabel")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.udpButton = QtWidgets.QPushButton(self.tab_2)
        self.udpButton.setGeometry(QtCore.QRect(0, 480, 791, 41))
        self.udpButton.setObjectName("udpButton")
        self.udpGroupBox = QtWidgets.QGroupBox(self.tab_2)
        self.udpGroupBox.setGeometry(QtCore.QRect(240, 0, 551, 471))
        self.udpGroupBox.setTitle("")
        self.udpGroupBox.setObjectName("udpGroupBox")
        self.labelVideo = QtWidgets.QLabel(self.udpGroupBox)
        self.labelVideo.setGeometry(QtCore.QRect(20, 30, 521, 431))
        self.labelVideo.setText("")
        self.labelVideo.setObjectName("labelVideo")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 221, 411))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 111, 17))
        self.label_4.setObjectName("label_4")
        self.udpStatusLabel = QtWidgets.QLabel(self.tab_2)
        self.udpStatusLabel.setGeometry(QtCore.QRect(10, 30, 221, 21))
        self.udpStatusLabel.setObjectName("udpStatusLabel")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.addFunctions()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tcpButton.setText(_translate("MainWindow", "Begin TCP transaction"))
        self.label.setText(_translate("MainWindow", "Connection info"))
        self.tcpStatusLabel.setText(_translate("MainWindow", "Status: Disconnected"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "TCP Socket"))
        self.udpButton.setText(_translate("MainWindow", "Begin UDP transaction"))
        self.label_4.setText(_translate("MainWindow", "Connection info"))
        self.udpStatusLabel.setText(_translate("MainWindow", "Status: Disconnected"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "UDP Socket"))

    def setImage(self, image):
        self.labelVideo.setPixmap(image)
        print("Image set")
        return 0

    def sendChoice(self, choice):
        errorCode, port = Client.sendChoice(choice)
        print("Client.port = ", port)
        if choice == 1:
            if errorCode == 0:
                labelText = "Server = localhost\nPort = " + str(port) +"\nProtocol = TCP"
                self.label_2.setText(labelText)
                self.sendTCP(port)
            else:
                self.label_2.setText("Connection error")
        else:
            if errorCode == 0:
                labelText = "Server = localhost\nPort = " + str(port) +"\nProtocol = UDP"
                self.label_3.setText(labelText)
                self.sendUDP(port)
            else:
                self.label_3.setText("Connection error")

    def sendTCP(self, port):
        print("sendTCP function enter")
        path = Client.useTCP(port)
        image = QtGui.QPixmap(path)
        self.labelFoto.setPixmap(image)

    def sendUDP(self, port):
        error, udpSocket = Client.connectUDP(port)
        if error == 1:
            return 1
        maxFrame = 100
        currentFrame = 0
        while currentFrame < maxFrame:
            image = Client.useUDP(udpSocket)
            currentFrame += 1
            try:
                (h,w,d) = image.shape
                print("Image shape")
                qimage = QtGui.QImage(image.data, h, w, 3*h, QtGui.QImage.Format_RGB888)
                print("image to qimage")
                qpixmap = QtGui.QPixmap(qimage)
                ##qpixmap = QtGui.QPixmap("Image.png")
                self.setImage(qpixmap)
            except:
                continue
            finally:
                app.processEvents()
            ##self.labelVideo.setPixmap(qpixmap)
        return 0


    def addFunctions(self):
        self.tcpButton.clicked.connect(lambda: self.sendChoice(1))
        self.udpButton.clicked.connect(lambda: self.sendChoice(2))

    def showStatus(self, conn):
        if conn == 1:
            self.tcpStatusLabel.setText("Status: Disconnected")
            self.udpStatusLabel.setText("Status: Disconnected")
        else:
            self.tcpStatusLabel.setText("Status: Connected")
            self.udpStatusLabel.setText("Status: Connected")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    connection = Client.connect()
    ui.showStatus(connection)

    sys.exit(app.exec_())