# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_video_playback_widget.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VideoPlaybackWidget(object):
    def setupUi(self, VideoPlaybackWidget):
        VideoPlaybackWidget.setObjectName("VideoPlaybackWidget")
        VideoPlaybackWidget.resize(593, 100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VideoPlaybackWidget.sizePolicy().hasHeightForWidth())
        VideoPlaybackWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(VideoPlaybackWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(VideoPlaybackWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.buttonFrame = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonFrame.sizePolicy().hasHeightForWidth())
        self.buttonFrame.setSizePolicy(sizePolicy)
        self.buttonFrame.setObjectName("buttonFrame")
        self.ff = QtWidgets.QHBoxLayout(self.buttonFrame)
        self.ff.setObjectName("ff")
        self.moveFirstButton = QtWidgets.QPushButton(self.buttonFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.moveFirstButton.sizePolicy().hasHeightForWidth())
        self.moveFirstButton.setSizePolicy(sizePolicy)
        self.moveFirstButton.setMinimumSize(QtCore.QSize(40, 40))
        self.moveFirstButton.setMaximumSize(QtCore.QSize(40, 40))
        self.moveFirstButton.setText("")
        self.moveFirstButton.setObjectName("moveFirstButton")
        self.ff.addWidget(self.moveFirstButton)
        self.movePrevButton = QtWidgets.QPushButton(self.buttonFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.movePrevButton.sizePolicy().hasHeightForWidth())
        self.movePrevButton.setSizePolicy(sizePolicy)
        self.movePrevButton.setMinimumSize(QtCore.QSize(40, 40))
        self.movePrevButton.setMaximumSize(QtCore.QSize(40, 40))
        self.movePrevButton.setText("")
        self.movePrevButton.setObjectName("movePrevButton")
        self.ff.addWidget(self.movePrevButton)
        self.playButton = QtWidgets.QPushButton(self.buttonFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playButton.sizePolicy().hasHeightForWidth())
        self.playButton.setSizePolicy(sizePolicy)
        self.playButton.setMinimumSize(QtCore.QSize(40, 40))
        self.playButton.setMaximumSize(QtCore.QSize(40, 40))
        self.playButton.setText("")
        self.playButton.setObjectName("playButton")
        self.ff.addWidget(self.playButton)
        self.moveNextButton = QtWidgets.QPushButton(self.buttonFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.moveNextButton.sizePolicy().hasHeightForWidth())
        self.moveNextButton.setSizePolicy(sizePolicy)
        self.moveNextButton.setMinimumSize(QtCore.QSize(40, 40))
        self.moveNextButton.setMaximumSize(QtCore.QSize(40, 40))
        self.moveNextButton.setText("")
        self.moveNextButton.setObjectName("moveNextButton")
        self.ff.addWidget(self.moveNextButton)
        self.moveLastButton = QtWidgets.QPushButton(self.buttonFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.moveLastButton.sizePolicy().hasHeightForWidth())
        self.moveLastButton.setSizePolicy(sizePolicy)
        self.moveLastButton.setMinimumSize(QtCore.QSize(40, 40))
        self.moveLastButton.setMaximumSize(QtCore.QSize(40, 40))
        self.moveLastButton.setText("")
        self.moveLastButton.setObjectName("moveLastButton")
        self.ff.addWidget(self.moveLastButton)
        self.horizontalLayout_2.addWidget(self.buttonFrame)
        self.timeLabel = QtWidgets.QLabel(self.frame)
        self.timeLabel.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy)
        self.timeLabel.setMinimumSize(QtCore.QSize(80, 40))
        self.timeLabel.setMaximumSize(QtCore.QSize(80, 40))
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.horizontalLayout_2.addWidget(self.timeLabel)
        self.playbackSlider = QtWidgets.QSlider(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playbackSlider.sizePolicy().hasHeightForWidth())
        self.playbackSlider.setSizePolicy(sizePolicy)
        self.playbackSlider.setOrientation(QtCore.Qt.Horizontal)
        self.playbackSlider.setObjectName("playbackSlider")
        self.horizontalLayout_2.addWidget(self.playbackSlider)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(VideoPlaybackWidget)
        QtCore.QMetaObject.connectSlotsByName(VideoPlaybackWidget)

    def retranslateUi(self, VideoPlaybackWidget):
        _translate = QtCore.QCoreApplication.translate
        VideoPlaybackWidget.setWindowTitle(_translate("VideoPlaybackWidget", "Form"))
        self.timeLabel.setText(_translate("VideoPlaybackWidget", "00:00:00"))

