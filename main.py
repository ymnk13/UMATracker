#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re, hashlib

from PyQt5 import QtCore
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QFrame, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QTransform, QColor

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

        self.videoPlaybackInit()
        self.blocklyInit()
        self.imgInit()
        self.menuInit()

    def videoPlaybackInit(self):
        self.videoPlaybackWidget.hide()

        self.videoPlayStopButton.clicked.connect(self.videoPlayStopButtonClicked)
        self.videoGoHeadButton.clicked.connect(self.videoGoHeadButtonClicked)
        self.videoGoLastButton.clicked.connect(self.videoGoLastButtonClicked)

        self.videoGoForwardButton.clicked.connect(self.videoGoForwardButtonClicked)
        self.videoGoBackwardButton.clicked.connect(self.videoGoBackwardButtonClicked)
        self.videoGoForwardButton.setAutoRepeat(True)
        self.videoGoBackwardButton.setAutoRepeat(True)
        self.videoGoForwardButton.setAutoRepeatInterval(10)
        self.videoGoBackwardButton.setAutoRepeatInterval(10)

        self.videoPlaybackSlider.actionTriggered.connect(self.videoPlaybackSliderActionTriggered)

        self.videoPlaybackTimer = QtCore.QTimer(parent=self.videoPlaybackWidget)
        self.videoPlaybackTimer.timeout.connect(self.videoPlayback)

    def videoPlayStopButtonClicked(self):
        if self.videoPlaybackTimer.isActive():
            self.videoPlaybackTimer.stop()
            self.blocklyEvaluationTimer.start()
        else:
            maxFrames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if self.videoPlaybackSlider.value() is not maxFrames:
                self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

                self.videoPlaybackTimer.setInterval(1000.0/self.fps)
                self.videoPlaybackTimer.start()
                self.blocklyEvaluationTimer.stop()

    def videoGoHeadButtonClicked(self):
        self.videoPlaybackTimer.stop()
        if self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

            self.videoPlaybackSlider.setValue(0)

            self.setFrame(frame)

    def videoGoLastButtonClicked(self):
        self.videoPlaybackTimer.stop()
        if self.cap.isOpened():
            maxFrames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # TODO: 行儀の悪い映像だと，末尾のあたりの取得に（ここではsetの時点で）失敗・一時フリーズする．
            #       しかも，これといったエラーが出ずに進行．
            #       要検証．
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, maxFrames)
            ret, frame = self.cap.read()

            self.videoPlaybackSlider.setValue(maxFrames)

            self.setFrame(frame)

    def videoGoForwardButtonClicked(self):
        self.videoPlaybackTimer.stop()
        if self.cap.isOpened():
            nextFrame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            maxFrames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if nextFrame <= maxFrames:
                # TODO: 行儀の悪い映像だと，末尾のあたりの取得に（ここではsetの時点で）失敗・一時フリーズする．
                #       しかも，これといったエラーが出ずに進行．
                #       要検証．
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, nextFrame)
                ret, frame = self.cap.read()

                self.videoPlaybackSlider.setValue(nextFrame)

                self.setFrame(frame)

    def videoGoBackwardButtonClicked(self):
        self.videoPlaybackTimer.stop()
        if self.cap.isOpened():
            nextFrame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            beforeFrame = nextFrame - 2
            if beforeFrame >= 0:
                # TODO: 行儀の悪い映像だと，末尾のあたりの取得に（ここではsetの時点で）失敗・一時フリーズする．
                #       しかも，これといったエラーが出ずに進行．
                #       要検証．
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, beforeFrame)
                ret, frame = self.cap.read()

                self.videoPlaybackSlider.setValue(beforeFrame)

                self.setFrame(frame)

    def videoPlaybackSliderActionTriggered(self, action):
        logger.debug("Action: {0}".format(action))
        self.videoPlaybackTimer.stop()
        if self.cap.isOpened():
            # TODO: 行儀の悪い映像だと，末尾のあたりの取得に（ここではsetの時点で）失敗・一時フリーズする．
            #       しかも，これといったエラーが出ずに進行．
            #       要検証．
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.videoPlaybackSlider.value())
            ret, frame = self.cap.read()

            self.setFrame(frame)

    def videoPlayback(self):
        if self.cap.isOpened():
            nextFrame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            # TODO: 行儀の悪い映像だと，末尾のあたりの取得に（ここではreadの時点で）失敗・一時フリーズする．
            #       しかも，これといったエラーが出ずに進行．
            #       要検証．
            ret, frame = self.cap.read()

            if nextFrame%self.fps is 0:
                self.videoPlaybackSlider.setValue(nextFrame)

            self.setFrame(frame)

    def setFrame(self, frame):
        if frame is not None:
            self.cv_img = frame
            self.updateInputGraphicsView()
            self.evaluateSelectedBlock()
        else:
            self.videoPlaybackSlider.setValue(self.videoPlaybackSlider.maximum())
            self.videoPlaybackTimer.stop()
            self.blocklyEvaluationTimer.start()

    def blocklyInit(self):
        self.blocklyWebView.setUrl(QtCore.QUrl(filePath.blocklyURL))

        self.blocklyEvaluationTimer = QtCore.QTimer(parent=self.blocklyWebView)
        self.blocklyEvaluationTimer.setInterval(1*1000)
        self.blocklyEvaluationTimer.timeout.connect(self.evaluateSelectedBlock)
        self.blocklyEvaluationTimer.start()

        self.filterClassHash = None
        self.filter = None

    def imgInit(self):
        self.cap = None
        self.cv_img = cv2.imread(os.path.join(filePath.sampleDataPath,"color_filter_test.png"))

        self.inputScene = QGraphicsScene()
        self.inputGraphicsView.setScene(self.inputScene)
        self.inputGraphicsView.resizeEvent = self.inputGraphicsViewResized

        self.inputScene.mousePressEvent = self.inputSceneClicked

        self.outputScene = QGraphicsScene()
        self.outputGraphicsView.setScene(self.outputScene)
        self.outputGraphicsView.resizeEvent = self.outputGraphicsViewResized

        qimg = misc.cvMatToQImage(self.cv_img)
        pixmap = QPixmap.fromImage(qimg)
        self.inputScene.addPixmap(pixmap)

    def menuInit(self):
        self.actionOpenVideo.triggered.connect(self.openVideoFile)
        self.actionOpenImage.triggered.connect(self.openImageFile)

        self.actionOpenBlockData.triggered.connect(self.openBlockFile)
        self.actionSaveBlockData.triggered.connect(self.saveBlockFile)

        self.actionSaveFilterData.triggered.connect(self.saveFilterFile)

    def releaseVideoCapture(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def openVideoFile(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Open Video File', filePath.userDir)

        if len(filename) is not 0:
            self.releaseVideoCapture()
            self.cap = cv2.VideoCapture(misc.utfToSystemStr(filename))

            self.videoPlaybackWidget.show()
            self.videoPlaybackSlider.setRange(0, self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if self.cap.isOpened():
                ret, frame = self.cap.read()

                self.cv_img = frame
                self.updateInputGraphicsView()

                # Initialize Filter when opening new file.
                self.filterClassHash = None

    def openImageFile(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Open Image File', filePath.userDir)

        if len(filename) is not 0:
            self.cv_img = cv2.imread(misc.utfToSystemStr(filename))
            self.videoPlaybackWidget.hide()

            self.updateInputGraphicsView()
            self.releaseVideoCapture()

            # Initialize Filter when opening new file.
            self.filterClassHash = None

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

    def inputSceneClicked(self, event):
        pos = event.scenePos().toPoint()
        item = self.inputScene.itemAt(pos, QTransform())

        img = item.pixmap().toImage()
        pix = img.pixel(pos)
        rgb = QColor(pix).name()
        logger.debug("Selected pixel color: {0}".format(rgb))

        frame = self.blocklyWebView.page().mainFrame()
        frame.evaluateJavaScript("Apps.setColorFilterBlock('{0}');".format(rgb))

    def openBlockFile(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Open Block File', filePath.userDir, "Block files (*.block)")

        if len(filename) is not 0:
            logger.debug("Opening Block file: {0}".format(filename))

            with open(misc.utfToSystemStr(filename)) as f:
                text = f.read()
                text = re.sub(r"[\n\r]","",text)

                frame = self.blocklyWebView.page().mainFrame()
                script = "Apps.setBlockData('{0}');".format(text)
                ret = frame.evaluateJavaScript(script)

    def saveBlockFile(self):
        filename, _ = QFileDialog.getSaveFileName(None, 'Save Block File', filePath.userDir, "Block files (*.block)")

        if len(filename) is not 0:
            logger.debug("Saving Block file: {0}".format(filename))

            with open(misc.utfToSystemStr(filename), mode="w") as f:
                frame = self.blocklyWebView.page().mainFrame()
                text = frame.evaluateJavaScript("Apps.getBlockData();")

                f.write(text)

    def saveFilterFile(self):
        filename, _ = QFileDialog.getSaveFileName(None, 'Save Filter File', filePath.userDir, "Filter files (*.filter)")

        if len(filename) is not 0:
            logger.debug("Saving Filter file: {0}".format(filename))

            with open(misc.utfToSystemStr(filename), mode="w") as f:
                frame = self.blocklyWebView.page().mainFrame()
                self.processSequence(frame)

                text = frame.evaluateJavaScript("Apps.getCodeFromWorkspace();")
                if text is None:
                    return False

                text = self.parseToClass(text)
                f.write(text)

    def inputGraphicsViewResized(self, event=None):
        self.inputGraphicsView.fitInView(self.inputScene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def outputGraphicsViewResized(self, event=None):
        self.outputGraphicsView.fitInView(self.outputScene.sceneRect(), QtCore.Qt.KeepAspectRatio)


    def parseToClass(self, text):
        lines = text.split("\n")
        indents = "    "

        classMemberPattern = r"^#"

        classMembers = []
        filterOperations = []
        for line in lines:
            if re.match(classMemberPattern, line):
                classMembers.append(indents + indents + line.lstrip("#"))
            else:
                filterOperations.append(indents + indents + line)
        classMembers.append(indents + indents + "return")
        filterOperations.append(indents + indents + "return {output}")

        classMenbersStr = "\n".join(classMembers)
        filterOperationsStr = "\n".join(filterOperations)

        constructorStr = "\n".join([indents + "def __init__(self, im_input):", classMenbersStr])
        filterFuncStr  = "\n".join([indents + "def filterFunc(self, im_input):", filterOperationsStr])

        filterOperationClassStr = "\n".join(["class filterOperation:", constructorStr, filterFuncStr])

        return filterOperationClassStr.format(input="im_input", output="im_output")


    def evaluateSelectedBlock(self):
        im_output = None

        frame = self.blocklyWebView.page().mainFrame()
        self.processSequence(frame)

        text = frame.evaluateJavaScript("Apps.getCodeFromSelectedBlock();")
        if text is None:
            return False

        text = self.parseToClass(text)
        logger.debug("Generated Code: {0}".format(text))

        # TODO: あまりにも大きいイメージは縮小しないと処理がなかなか終わらない
        #       ので，そうしたほうがいい．

        textHash = hashlib.md5(text.encode())
        if self.filterClassHash != textHash:
            self.filterClassHash = textHash
            try:
                exec(text)
                self.filter = filterOperation(self.cv_img)
            except Exception as e:
                logger.debug("Block Evaluation Error: {0}".format(e))

        try:
            im_output = self.filter.filterFunc(self.cv_img)
        except Exception as e:
            logger.debug("Filter execution Error: {0}".format(e))

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

