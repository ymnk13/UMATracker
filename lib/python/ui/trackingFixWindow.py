# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trackingFixWindow.ui'
#
# Created: Tue Jun 30 19:07:23 2015
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class trackingFixWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(516, 399)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.videoController = QtWidgets.QWidget(self.centralWidget)
        self.videoController.setMinimumSize(QtCore.QSize(0, 32))
        self.videoController.setMaximumSize(QtCore.QSize(16777215, 32))
        self.videoController.setObjectName("videoController")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.videoController)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.videoGoBackwardButton = QtWidgets.QPushButton(self.videoController)
        self.videoGoBackwardButton.setMaximumSize(QtCore.QSize(32, 32))
        self.videoGoBackwardButton.setObjectName("videoGoBackwardButton")
        self.horizontalLayout.addWidget(self.videoGoBackwardButton)
        self.videoPlayButton = QtWidgets.QPushButton(self.videoController)
        self.videoPlayButton.setMaximumSize(QtCore.QSize(32, 32))
        self.videoPlayButton.setObjectName("videoPlayButton")
        self.horizontalLayout.addWidget(self.videoPlayButton)
        self.videoGoForwardButton = QtWidgets.QPushButton(self.videoController)
        self.videoGoForwardButton.setMaximumSize(QtCore.QSize(32, 32))
        self.videoGoForwardButton.setObjectName("videoGoForwardButton")
        self.horizontalLayout.addWidget(self.videoGoForwardButton)
        self.videoStopButton = QtWidgets.QPushButton(self.videoController)
        self.videoStopButton.setMaximumSize(QtCore.QSize(32, 32))
        self.videoStopButton.setObjectName("videoStopButton")
        self.horizontalLayout.addWidget(self.videoStopButton)
        spacerItem = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.videoPlaybackSlider = QtWidgets.QSlider(self.videoController)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoPlaybackSlider.sizePolicy().hasHeightForWidth())
        self.videoPlaybackSlider.setSizePolicy(sizePolicy)
        self.videoPlaybackSlider.setStyleSheet("QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: white;\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background: #66e;\n"
"background: #bbf;\n"
"border: 1px solid #777;\n"
"height: 10px;\n"
"border-radius: 0px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"background: #fff;\n"
"border: 1px solid #777;\n"
"height: 10px;\n"
"border-radius: 0px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"//background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"//   stop:0 #eee, stop:1 #ccc);\n"
"//border: 1px solid #777;\n"
"//width: 0px;\n"
"//margin-top: -2px;\n"
"//margin-bottom: -2px;\n"
"//border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #fff, stop:1 #ddd);\n"
"border: 1px solid #444;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 4px;\n"
"}")
        self.videoPlaybackSlider.setProperty("value", 20)
        self.videoPlaybackSlider.setSliderPosition(20)
        self.videoPlaybackSlider.setTracking(True)
        self.videoPlaybackSlider.setOrientation(QtCore.Qt.Horizontal)
        self.videoPlaybackSlider.setInvertedAppearance(False)
        self.videoPlaybackSlider.setInvertedControls(False)
        self.videoPlaybackSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.videoPlaybackSlider.setObjectName("videoPlaybackSlider")
        self.horizontalLayout.addWidget(self.videoPlaybackSlider)
        self.verticalLayout.addWidget(self.videoController)
        self.dataController = QtWidgets.QWidget(self.centralWidget)
        self.dataController.setObjectName("dataController")
        self.gridLayout = QtWidgets.QGridLayout(self.dataController)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.datatTableBox = QtWidgets.QGroupBox(self.dataController)
        self.datatTableBox.setAutoFillBackground(False)
        self.datatTableBox.setObjectName("datatTableBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.datatTableBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableView = QtWidgets.QTableView(self.datatTableBox)
        self.tableView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setAutoFillBackground(False)
        self.tableView.setObjectName("tableView")
        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.datatTableBox, 0, 0, 1, 1)
        self.dataGraphicsBox = QtWidgets.QGroupBox(self.dataController)
        self.dataGraphicsBox.setObjectName("dataGraphicsBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dataGraphicsBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.graphicsView = QtWidgets.QGraphicsView(self.dataGraphicsBox)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_3.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.dataGraphicsBox, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.dataController)
        self.debugLabel = QtWidgets.QLabel(self.centralWidget)
        self.debugLabel.setObjectName("debugLabel")
        self.verticalLayout.addWidget(self.debugLabel)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 516, 22))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.videoGoBackwardButton.setText(_translate("MainWindow", "<<"))
        self.videoPlayButton.setText(_translate("MainWindow", "P"))
        self.videoPlayButton.setShortcut(_translate("MainWindow", "Meta+S"))
        self.videoGoForwardButton.setText(_translate("MainWindow", ">>"))
        self.videoStopButton.setText(_translate("MainWindow", "S"))
        self.datatTableBox.setTitle(_translate("MainWindow", "データ"))
        self.dataGraphicsBox.setTitle(_translate("MainWindow", "動画"))
        self.debugLabel.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = trackingFixWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

