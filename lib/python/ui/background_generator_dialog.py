#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, six, time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QDialog, QProgressDialog
from PyQt5.QtGui import QPixmap, QColor, QBrush, QImage
from PyQt5.QtCore import QRectF, QPointF, Qt

try:
    from ui_background_generator_dialog import Ui_BackgroundGeneratorDialog
except ImportError:
    from .ui_background_generator_dialog import Ui_BackgroundGeneratorDialog

import cv2

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

def cvMatToQImage(im_in):
    logger.debug('Input image type: {0}'.format(im_in.dtype))
    if len(im_in.shape) is 3:
        height, width, bytesPerComponent = im_in.shape
        bytesPerLine = bytesPerComponent * width;
        im_dst = cv2.cvtColor(im_in, cv2.COLOR_BGR2RGB)
        return QImage(im_dst.data, width, height, bytesPerLine, QImage.Format_RGB888)
    else:
        height, width = im_in.shape
        return QImage(im_in.data, width, height, width, QImage.Format_Indexed8)


class BackgroundGeneratorDialog(Ui_BackgroundGeneratorDialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        Ui_BackgroundGeneratorDialog.__init__(self)
        self.setupUi(self)

        self.videoPlaybackInit()
        self.imgInit()

        self.generateButton.pressed.connect(self.generateBackground)

    def closeEvent(self,event):
        pass

    def videoPlaybackInit(self):
        self.videoPlaybackWidget.frameChanged.connect(self.setFrame)

    def setFrame(self, frame):
        if frame is not None:

            self.cv_img = frame
            self.updateInputGraphicsView()

            if self.fgbg is not None:
                self.updateOutputGraphicsView()

    def imgInit(self):
        self.inputScene = QGraphicsScene()
        self.inputGraphicsView.setScene(self.inputScene)
        self.inputGraphicsView.resizeEvent = self.inputGraphicsViewResized

        self.outputScene = QGraphicsScene()
        self.outputGraphicsView.setScene(self.outputScene)
        self.outputGraphicsView.resizeEvent = self.outputGraphicsViewResized

        self.fgbg = None

    def openVideoFile(self, filePath = None):
        if len(filePath) is not 0:
            self.filePath = filePath

            ret = self.videoPlaybackWidget.openVideo(filePath)
            if ret == False:
                return False

            self.videoPlaybackWidget.show()
            self.filterClassHash = None

            return True

    def updateInputGraphicsView(self):
        self.inputScene.clear()
        # self.inputScene.removeItem(self.inputPixMapItem)
        qimg = cvMatToQImage(self.cv_img)
        self.inputPixMap = QPixmap.fromImage(qimg)

        rect = QtCore.QRectF(self.inputPixMap.rect())
        self.inputScene.setSceneRect(rect)
        self.outputScene.setSceneRect(rect)

        self.inputPixMapItem = QGraphicsPixmapItem(self.inputPixMap)
        # self.inputScene.setBackgroundBrush(QBrush(self.inputPixMap))
        self.inputScene.addItem(self.inputPixMapItem)

        self.inputGraphicsView.viewport().update()
        self.inputGraphicsViewResized()

    def updateOutputGraphicsView(self):
        if True:
            out_img = self.fgbg.apply(self.cv_img, learningRate=0)
        else:
            bg = self.fgbg.getBackgroundImage()
            out_img = cv2.absdiff(self.cv_img, bg)

        self.outputScene.clear()
        qimg = cvMatToQImage(out_img)
        self.outputPixMap = QPixmap.fromImage(qimg)

        rect = QtCore.QRectF(self.outputPixMap.rect())
        self.outputScene.setSceneRect(rect)

        self.outputPixMapItem = QGraphicsPixmapItem(self.outputPixMap)
        self.outputScene.addItem(self.outputPixMapItem)

        self.outputGraphicsView.viewport().update()
        self.outputGraphicsViewResized()

    def inputGraphicsViewResized(self, event=None):
        self.inputGraphicsView.fitInView(self.inputScene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def outputGraphicsViewResized(self, event=None):
        self.outputGraphicsView.fitInView(self.outputScene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def generateBackground(self):
        minFrame = self.videoPlaybackWidget.getMinRange()
        maxFrame = self.videoPlaybackWidget.getMaxRange()
        stride = self.strideSpinBox.value()
        numFrames = int((maxFrame-minFrame)/stride)
        progress = QProgressDialog("Generating background...", "Abort", 0, numFrames, self)

        progress.setWindowModality(Qt.WindowModal)

        fgbg = cv2.createBackgroundSubtractorMOG2()
        currentFrameNo = self.videoPlaybackWidget.currentFrameNo
        for i, frameNo in enumerate(range(minFrame, maxFrame+1, stride)):
            progress.setValue(i)
            if progress.wasCanceled():
                break

            ret, frame = self.videoPlaybackWidget.readFrame(frameNo)
            fgbg.apply(frame)

        if not progress.wasCanceled():
            self.fgbg = fgbg
            self.setFrame(self.cv_img)

        progress.setValue(numFrames)

        self.videoPlaybackWidget.currentFrameNo = currentFrameNo

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = BackgroundGeneratorDialog()
    Dialog.openVideoFile('leurre.avi')
    Dialog.show()
    sys.exit(app.exec_())

