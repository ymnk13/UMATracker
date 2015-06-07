#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsView,QGraphicsPixmapItem,QFrame, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

import cv2
import numpy as np

import filePath

sys.path.append( filePath.pythonLibDirPath )
import misc

sys.path.append( os.path.join(filePath.pythonLibDirPath, 'pycv') )
import filters

sys.path.append( os.path.join(filePath.pythonLibDirPath, 'ui') )
from MainWindowBase import *


# Log file setting.
# import logging
# logging.basicConfig(filename='MainWindow.log', level=logging.DEBUG)

# Log output setting.
# If handler = StreamHandler(), log will output into StandardOutput.
from logging import getLogger, NullHandler, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = NullHandler() if True else StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

class Ui_MainWindow(Ui_MainWindowBase):
    def setupUi(self, MainWindow, path):
        super(Ui_MainWindow, self).setupUi(MainWindow)

        self.blocklyInit()
        self.imgInit()
        self.menuInit()

    def blocklyInit(self):
        self.blocklyWebView.setUrl(QtCore.QUrl(filePath.blocklyURL))

        self.timer = QtCore.QTimer(parent=self.blocklyWebView)
        self.timer.setInterval(1*1000)
        self.timer.timeout.connect(self.evaluateSelectedBlock)
        self.timer.start()

    def imgInit(self):
        self.cap = None
        self.cv_img = cv2.imread(os.path.join(filePath.sampleDataPath,"color_filter_test.png"))

        self.inputScene = QGraphicsScene()
        self.inputGraphicsView.setScene(self.inputScene)
        self.inputGraphicsView.resizeEvent = self.inputGraphicsViewResized

        self.outputScene = QGraphicsScene()
        self.outputGraphicsView.setScene(self.outputScene)
        self.outputGraphicsView.resizeEvent = self.outputGraphicsViewResized

        qimg = misc.cvMatToQImage(self.cv_img)
        pixmap = QPixmap.fromImage(qimg)
        self.inputScene.addPixmap(pixmap)

    def menuInit(self):
        self.actionOpenVideo.triggered.connect(self.openVideoFile)
        self.actionOpenImage.triggered.connect(self.openImageFile)
        self.actionOpenBlockData.triggered.connect(self.openXMLFile)
        self.actionSaveBlockData.triggered.connect(self.saveXMLFile)

    def releaseVideoCapture(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def openVideoFile(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Open Video File', filePath.userDir)

        if len(filename) is not 0:
            self.releaseVideoCapture()
            self.cap = cv2.VideoCapture(misc.utfToSystemStr(filename))

            if self.cap.isOpened():
                ret, frame = self.cap.read()

                self.cv_img = frame
                self.updateInputGraphicsView()


    def openImageFile(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Open Image File', filePath.userDir)

        if len(filename) is not 0:
            self.cv_img = cv2.imread(misc.utfToSystemStr(filename))

            self.updateInputGraphicsView()
            self.releaseVideoCapture()

    def updateInputGraphicsView(self):
        self.inputScene.clear()
        qimg = misc.cvMatToQImage(self.cv_img)
        pixmap = QPixmap.fromImage(qimg)

        rect = QtCore.QRectF(pixmap.rect())
        self.inputScene.setSceneRect(rect)
        self.outputScene.setSceneRect(rect)

        self.inputScene.addPixmap(pixmap)

        self.inputGraphicsView.viewport().update()
        self.inputGraphicsViewResized()

    def openXMLFile(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Open XML File', filePath.userDir)

        if len(filename) is not 0:
            logger.debug("Opening XML file: {0}".format(filename))

    def saveXMLFile(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Save XML File', filePath.userDir)

    def inputGraphicsViewResized(self, event=None):
        self.inputGraphicsView.fitInView(self.inputScene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def outputGraphicsViewResized(self, event=None):
        self.outputGraphicsView.fitInView(self.outputScene.sceneRect(), QtCore.Qt.KeepAspectRatio)


    def evaluateSelectedBlock(self):
        im_output = None

        frame = self.blocklyWebView.page().mainFrame()
        self.processSequence(frame)

        text = frame.evaluateJavaScript("Apps.getSelectingCode()")
        if text is None:
            return False


        # TODO: あまりにも大きいイメージは縮小しないと処理がなかなか終わらない
        #       ので，そうしたほうがいい．
        im_input = self.cv_img


        logger.debug("Generated Code: {0}".format(text))
        try:
            exec(text)
        except Exception as e:
            logger.debug("Block Evaluation Error: {0}".format(e))


        if im_output is None:
            return False

        self.outputScene.clear()
        qimg = misc.cvMatToQImage(im_output)
        pixmap = QPixmap.fromImage(qimg)
        self.outputScene.addPixmap(pixmap)

        self.outputGraphicsView.viewport().update()
        self.outputGraphicsViewResized()

    def processSequence(self, frame):
        buttonExecute = frame.findFirstElement('#execute')
        script = frame.findFirstElement('#SCRIPT')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow,filePath.currentDirPath)
    MainWindow.show()
    sys.exit(app.exec_())

