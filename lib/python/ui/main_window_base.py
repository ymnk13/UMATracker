# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_window_base.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindowBase(object):
    def setupUi(self, MainWindowBase):
        MainWindowBase.setObjectName("MainWindowBase")
        MainWindowBase.resize(976, 580)
        MainWindowBase.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindowBase)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.blockEditorBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.blockEditorBox.sizePolicy().hasHeightForWidth())
        self.blockEditorBox.setSizePolicy(sizePolicy)
        self.blockEditorBox.setObjectName("blockEditorBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.blockEditorBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.blocklyWebView = QtWebKitWidgets.QWebView(self.blockEditorBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.blocklyWebView.sizePolicy().hasHeightForWidth())
        self.blocklyWebView.setSizePolicy(sizePolicy)
        self.blocklyWebView.setAcceptDrops(False)
        self.blocklyWebView.setUrl(QtCore.QUrl("about:blank"))
        self.blocklyWebView.setObjectName("blocklyWebView")
        self.verticalLayout.addWidget(self.blocklyWebView)
        self.videoPlaybackWidget = VideoPlaybackWidget(self.blockEditorBox)
        self.videoPlaybackWidget.setObjectName("videoPlaybackWidget")
        self.verticalLayout.addWidget(self.videoPlaybackWidget)
        self.horizontalLayout.addWidget(self.blockEditorBox)
        self.graphicsBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.graphicsBox.sizePolicy().hasHeightForWidth())
        self.graphicsBox.setSizePolicy(sizePolicy)
        self.graphicsBox.setObjectName("graphicsBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.graphicsBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.inputGraphicsView = QtWidgets.QGraphicsView(self.graphicsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.inputGraphicsView.sizePolicy().hasHeightForWidth())
        self.inputGraphicsView.setSizePolicy(sizePolicy)
        self.inputGraphicsView.setAcceptDrops(False)
        self.inputGraphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.inputGraphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.inputGraphicsView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.inputGraphicsView.setObjectName("inputGraphicsView")
        self.verticalLayout_2.addWidget(self.inputGraphicsView)
        self.outputGraphicsView = QtWidgets.QGraphicsView(self.graphicsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.outputGraphicsView.sizePolicy().hasHeightForWidth())
        self.outputGraphicsView.setSizePolicy(sizePolicy)
        self.outputGraphicsView.setAcceptDrops(False)
        self.outputGraphicsView.setObjectName("outputGraphicsView")
        self.verticalLayout_2.addWidget(self.outputGraphicsView)
        self.horizontalLayout.addWidget(self.graphicsBox)
        MainWindowBase.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowBase)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 976, 21))
        self.menubar.setObjectName("menubar")
        self.menuFiles = QtWidgets.QMenu(self.menubar)
        self.menuFiles.setObjectName("menuFiles")
        self.menuBackground = QtWidgets.QMenu(self.menubar)
        self.menuBackground.setObjectName("menuBackground")
        MainWindowBase.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowBase)
        self.statusbar.setObjectName("statusbar")
        MainWindowBase.setStatusBar(self.statusbar)
        self.actionOpenVideo = QtWidgets.QAction(MainWindowBase)
        self.actionOpenVideo.setObjectName("actionOpenVideo")
        self.actionOpenImage = QtWidgets.QAction(MainWindowBase)
        self.actionOpenImage.setObjectName("actionOpenImage")
        self.actionOpenBlockData = QtWidgets.QAction(MainWindowBase)
        self.actionOpenBlockData.setObjectName("actionOpenBlockData")
        self.actionSaveBlockData = QtWidgets.QAction(MainWindowBase)
        self.actionSaveBlockData.setObjectName("actionSaveBlockData")
        self.actionQuit = QtWidgets.QAction(MainWindowBase)
        self.actionQuit.setObjectName("actionQuit")
        self.actionSaveFilterData = QtWidgets.QAction(MainWindowBase)
        self.actionSaveFilterData.setObjectName("actionSaveFilterData")
        self.actionOpenFilterData = QtWidgets.QAction(MainWindowBase)
        self.actionOpenFilterData.setObjectName("actionOpenFilterData")
        self.actionCreateBackground = QtWidgets.QAction(MainWindowBase)
        self.actionCreateBackground.setObjectName("actionCreateBackground")
        self.actionEnable_Disable = QtWidgets.QAction(MainWindowBase)
        self.actionEnable_Disable.setObjectName("actionEnable_Disable")
        self.menuFiles.addAction(self.actionOpenVideo)
        self.menuFiles.addAction(self.actionOpenImage)
        self.menuFiles.addSeparator()
        self.menuFiles.addAction(self.actionSaveFilterData)
        self.menuFiles.addAction(self.actionOpenFilterData)
        self.menuFiles.addSeparator()
        self.menuFiles.addAction(self.actionQuit)
        self.menuBackground.addAction(self.actionCreateBackground)
        self.menubar.addAction(self.menuFiles.menuAction())
        self.menubar.addAction(self.menuBackground.menuAction())

        self.retranslateUi(MainWindowBase)
        self.actionQuit.triggered.connect(MainWindowBase.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindowBase)

    def retranslateUi(self, MainWindowBase):
        _translate = QtCore.QCoreApplication.translate
        MainWindowBase.setWindowTitle(_translate("MainWindowBase", "MainWindow"))
        self.blockEditorBox.setTitle(_translate("MainWindowBase", "Block Editor"))
        self.graphicsBox.setTitle(_translate("MainWindowBase", "I/O"))
        self.menuFiles.setTitle(_translate("MainWindowBase", "Files"))
        self.menuBackground.setTitle(_translate("MainWindowBase", "Background"))
        self.actionOpenVideo.setText(_translate("MainWindowBase", "Open Video"))
        self.actionOpenImage.setText(_translate("MainWindowBase", "Open Image"))
        self.actionOpenBlockData.setText(_translate("MainWindowBase", "Open Block Data"))
        self.actionSaveBlockData.setText(_translate("MainWindowBase", "Save Block Data"))
        self.actionQuit.setText(_translate("MainWindowBase", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindowBase", "Ctrl+Q"))
        self.actionSaveFilterData.setText(_translate("MainWindowBase", "Save Filter Data"))
        self.actionOpenFilterData.setText(_translate("MainWindowBase", "Open Filter Data"))
        self.actionCreateBackground.setText(_translate("MainWindowBase", "Create"))
        self.actionEnable_Disable.setText(_translate("MainWindowBase", "Enable/Disable"))

from PyQt5 import QtWebKitWidgets
from .video_playback_widget import VideoPlaybackWidget