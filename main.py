#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import re, hashlib, json

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    currentDirPath = sys._MEIPASS
    print(currentDirPath)
    if os.name == 'nt':
        import win32api
        win32api.SetDllDirectory(sys._MEIPASS)
elif __file__:
    currentDirPath = os.getcwd()

sampleDataPath = os.path.join(currentDirPath,"data")
userDir        = os.path.expanduser('~')

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QMainWindow, QDialog, QProgressDialog
from PyQt5.QtGui import QPixmap, QColor, QBrush, QIcon
from PyQt5.QtCore import QRectF, QPointF, Qt

from lib.python.ui.main_window_base import Ui_MainWindowBase
from lib.python.ui.resizable_object import ResizableRect, ResizableEllipse
from lib.python.ui.background_generator_dialog import BackgroundGeneratorDialog
from lib.python.ui.movable_polygon import MovablePolygon

from lib.python import misc
import icon

import cv2
from lib.python.FilterIO.FilterIO import FilterIO
from lib.python.PythonClassGenerator.ClassTextGenerator import ClassTextGenerator

#For block evaluation, DO NOT REMOVE!#
import numpy as np
from lib.python.pycv import filters
######################################

import urllib.request
blocklyURL = "file:" + urllib.request.pathname2url(os.path.join(currentDirPath,"lib","editor","index.html"))

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


class Ui_MainWindow(QMainWindow, Ui_MainWindowBase):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        self.videoPlaybackInit()
        self.blocklyInit()
        self.imgInit()
        self.menuInit()

    def videoPlaybackInit(self):
        self.videoPlaybackWidget.hide()
        self.videoPlaybackWidget.frameChanged.connect(self.setFrame, type=Qt.QueuedConnection)
        self.filePath = None

    def blocklyInit(self):
        self.blocklyWebView.setUrl(QtCore.QUrl(blocklyURL))
        self.blocklyEvaluationTimer = QtCore.QTimer(parent=self.blocklyWebView)
        self.blocklyEvaluationTimer.setInterval(1*100)
        self.blocklyEvaluationTimer.timeout.connect(self.evaluateSelectedBlock)
        self.blocklyEvaluationTimer.start()

        self.filterClassHash = None
        self.filter = None
        self.selectedBlockID = None
        self.fgbg = None

    def imgInit(self):
        self.cv_img = cv2.imread(os.path.join(sampleDataPath,"color_filter_test.png"))
        self.im_output = None

        self.inputScene = QGraphicsScene()
        self.inputGraphicsView.setScene(self.inputScene)
        self.inputGraphicsView.resizeEvent = self.inputGraphicsViewResized

        self.outputPixmap = None
        self.outputScene = QGraphicsScene()
        self.outputGraphicsView.setScene(self.outputScene)
        self.outputGraphicsView.resizeEvent = self.outputGraphicsViewResized

        qimg = misc.cvMatToQImage(self.cv_img)
        self.inputPixmap = QPixmap.fromImage(qimg)
        self.inputPixmapItem = QGraphicsPixmapItem(self.inputPixmap)
        self.inputPixmapItem.mousePressEvent = self.getPixmapItemClickedPos
        self.inputScene.addItem(self.inputPixmapItem)

    def menuInit(self):
        self.actionOpenVideo.triggered.connect(self.openVideoFile)
        self.actionOpenImage.triggered.connect(self.openImageFile)
        self.actionSaveVideo.triggered.connect(self.saveVideoFile)

        self.actionSaveFilterData.triggered.connect(self.saveFilterFile)
        self.actionOpenFilterData.triggered.connect(self.openFilterFile)

        self.actionCreateBackground.triggered.connect(self.createBackground)

    def dragEnterEvent(self,event):
        event.acceptProposedAction()

    def dropEvent(self,event):
        mime = event.mimeData()
        if mime.hasUrls():
            urls = mime.urls()
            if len(urls) > 0:
                self.processDropedFile(urls[0].toLocalFile())

        event.acceptProposedAction()

    def closeEvent(self,event):
        pass

    def processDropedFile(self,filePath):
        root,ext = os.path.splitext(filePath)
        if ext == ".filter":
            # Read Filter
            self.openFilterFile(filePath=filePath)
            return
        elif self.openImageFile(filePath=filePath):
            return
        elif self.openVideoFile(filePath=filePath):
            return

    def setFrame(self, frame):
        if frame is not None:
            self.cv_img = frame
            self.updateInputGraphicsView()
            self.evaluateSelectedBlock()

    def setRectangleParameterToBlock(self, topLeft, bottomRight):
        height, width, dim = self.cv_img.shape

        array = [
                [topLeft.x()/width, topLeft.y()/height],
                [bottomRight.x()/width, bottomRight.y()/height]
                ]
        parameters = {'array': '{0}'.format(array)}
        string = json.dumps({k: str(v) for k, v in parameters.items()})
        webFrame = self.blocklyWebView.page().mainFrame()
        webFrame.evaluateJavaScript("Apps.setValueToSelectedBlock({0});".format(string))

    def setArrayParameterToBlock(self, array):
        height, width, dim = self.cv_img.shape

        array = [[x[0]/width, x[1]/height] for x in array]
        parameters = {'array': '{0}'.format(array)}
        string = json.dumps({k: str(v) for k, v in parameters.items()})
        webFrame = self.blocklyWebView.page().mainFrame()
        webFrame.evaluateJavaScript("Apps.setValueToSelectedBlock({0});".format(string))

    def createBackground(self, activated=False):
        if self.videoPlaybackWidget.isOpened():
            self.videoPlaybackWidget.stop()

            bg_dialog = BackgroundGeneratorDialog(self)
            bg_dialog.setWindowModality(Qt.WindowModal)
            bg_dialog.videoPlaybackWidget.copySource(self.videoPlaybackWidget)

            res = bg_dialog.exec()

            if res == QDialog.Accepted:
                self.fgbg = bg_dialog.fgbg.getBackgroundImage()

    def openVideoFile(self, activated=False, filePath = None):
        if filePath is None:
            filePath, _ = QFileDialog.getOpenFileName(None, 'Open Video File', userDir)

        if len(filePath) is not 0:
            self.filePath = filePath
            self.fgbg = None

            ret = self.videoPlaybackWidget.openVideo(filePath)
            if ret == False:
                return False

            self.videoPlaybackWidget.show()
            self.filterClassHash = None

            return True

    def openImageFile(self, activated=False, filePath = None):
        if filePath == None:
            filePath, _ = QFileDialog.getOpenFileName(None, 'Open Image File', userDir)

        if len(filePath) is not 0:
            self.filePath = filePath
            img = cv2.imread(filePath)
            if img is None:
                return False

            self.cv_img = img
            self.fgbg = None

            self.videoPlaybackWidget.hide()
            self.updateInputGraphicsView()

            # Initialize Filter when opening new file.
            self.filterClassHash = None

            return True
        else:
            return False

    def updateInputGraphicsView(self):
        self.inputScene.removeItem(self.inputPixmapItem)
        qimg = misc.cvMatToQImage(self.cv_img)
        self.inputPixmap = QPixmap.fromImage(qimg)

        rect = QtCore.QRectF(self.inputPixmap.rect())
        self.inputScene.setSceneRect(rect)

        self.inputPixmapItem = QGraphicsPixmapItem(self.inputPixmap)
        self.inputScene.addItem(self.inputPixmapItem)

        self.inputGraphicsView.viewport().update()
        self.inputGraphicsViewResized()

    def getPixmapItemClickedPos(self, event):
        pos = event.scenePos().toPoint()
        print(pos)

    def inputPixmapItemClicked(self, event):
        pos = event.scenePos().toPoint()

        img = self.inputPixmap.toImage()
        pix = img.pixel(pos)
        rgb = QColor(pix).name()
        logger.debug("Selected pixel color: {0}".format(rgb))

        parameters = {
                'Color': rgb,
                }
        string = json.dumps(parameters)
        webFrame = self.blocklyWebView.page().mainFrame()
        webFrame.evaluateJavaScript("Apps.setValueToSelectedBlock({0});".format(string))

    def openFilterFile(self, activated=False, filePath = None):
        if filePath is None:
            filePath, _ = QFileDialog.getOpenFileName(None, 'Open Block File', userDir, "Block files (*.filter)")

        if len(filePath) is not 0:
            logger.debug("Open Filter file: {0}".format(filePath))

            filterIO = FilterIO(filePath)
            self.fgbg = filterIO.getBackgroundImg()

            exec(filterIO.getFilterCode(), globals())

            blockXML = re.sub(r"[\n\r]",'', filterIO.getBlockXMLData())
            frame = self.blocklyWebView.page().mainFrame()
            frame.evaluateJavaScript("Apps.setBlockData('{0}');".format(blockXML))

    def saveFilterFile(self):
        self.blocklyEvaluationTimer.stop()
        if self.filePath is not None:
            candidateFilePath = os.path.splitext(self.filePath)[0] + '.filter'
        else:
            candidateFilePath = userDir
        filePath, _ = QFileDialog.getSaveFileName(None, 'Save Filter File', candidateFilePath, "Filter files (*.filter)")

        if len(filePath) is not 0:
            logger.debug("Saving Filter file: {0}".format(filePath))

            frame = self.blocklyWebView.page().mainFrame()

            filterIO = FilterIO()
            filterIO.setBlockXMLData(frame.evaluateJavaScript("Apps.getBlockData();"))

            filterClassText = self.parseToClass(frame.evaluateJavaScript("Apps.getCodeFromWorkspace();"))
            filterIO.setFilterCode(filterClassText)

            filterIO.setBackgroundImg(self.fgbg)

            filterIO.save(filePath)

        self.blocklyEvaluationTimer.start()

    def inputGraphicsViewResized(self, event=None):
        self.inputGraphicsView.fitInView(QtCore.QRectF(self.inputPixmap.rect()), QtCore.Qt.KeepAspectRatio)

    def outputGraphicsViewResized(self, event=None):
        if self.outputPixmap is None:
            self.outputGraphicsView.fitInView(self.outputScene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        else:
            self.outputGraphicsView.fitInView(QtCore.QRectF(self.outputPixmap.rect()), QtCore.Qt.KeepAspectRatio)

    def parseToClass(self, text):
        additionalText = """#self.fgbg = None
#self.resize_flag = {resize_flag}
#if self.resize_flag:
#    im_input = cv2.pyrDown(im_input)
if self.resize_flag:
    {input} = cv2.pyrDown({input})
if self.fgbg is not None:
    {input} = cv2.absdiff({input}, self.fgbg)
""".format(resize_flag=self.actionResize.isChecked(), input="{input}")
        text = additionalText + text

        lines = text.split("\n")
        classMemberPattern = r"^#"

        classMembers = []
        filterOperations = []

        for line in lines:
            if re.match(classMemberPattern, line):
                classMembers.append(line.lstrip("#"))
            else:
                filterOperations.append(line)

        generator = ClassTextGenerator('filterOperation')
        generator.functions['__init__']['lines'] = classMembers
        generator.functions['__init__']['args'] = ['im_input']

        filterOperations.append('return {output}')
        generator.addFunction('filterFunc', filterOperations, args=['im_input'], returnVal=True)

        return generator.generate().format(input="im_input", output="im_output")

    def reflectSelectedBlockStateIntoUI(self):
        webFrame = self.blocklyWebView.page().mainFrame()

        data = webFrame.evaluateJavaScript("Apps.getBlockTypeFromSelectedBlock();")
        if data is None:
            self.resetSceneAction(self.selectedBlockID)
            self.selectedBlockID = None
            return

        blockType = data['type']
        blockID = data['id']
        blockAttributes = data['attributes']
        if self.selectedBlockID != blockID:
            self.resetSceneAction(self.selectedBlockID)
            self.selectedBlockID = blockID

        if 'regionSelector' in blockAttributes:
            parameters = webFrame.evaluateJavaScript("Apps.getValueFromSelectedBlock();")

            graphicsItem = self.getGrphicsItemFromInputScene(blockID)

            if graphicsItem is not None:
                if graphicsItem.isVisible() is False:
                    graphicsItem.show()
            else:
                height, width, dim = self.cv_img.shape
                array = [[x[0]*width, x[1]*height] for x in eval(parameters['array'])]

                if blockType == "rectRegionSelector":
                    graphicsItem = ResizableRect()
                elif blockType == "ellipseRegionSelector":
                    graphicsItem = ResizableEllipse()
                elif blockType == "polyRegionSelector":
                    graphicsItem = MovablePolygon()
                self.inputScene.addItem(graphicsItem)
                graphicsItem.setPoints(array)

                graphicsItem.setObjectName(blockID)
                graphicsItem.geometryChange.connect(self.setArrayParameterToBlock)

            self.updateInputGraphicsView()

        elif 'colorSelector' in blockAttributes:
            self.inputPixmapItem.mousePressEvent = self.inputPixmapItemClicked
        else:
            self.inputPixmapItem.mousePressEvent = self.getPixmapItemClickedPos

    def resetSceneAction(self, blockID):
        graphicsItem = self.getGrphicsItemFromInputScene(blockID)
        if graphicsItem is not None:
            graphicsItem.hide()
        self.inputPixmapItem.mousePressEvent = QGraphicsPixmapItem(self.inputPixmapItem).mousePressEvent

    def getGrphicsItemFromInputScene(self, blockID):
        try:
            int(blockID)
        except:
            return None

        for item in self.inputScene.items():
            # QGraphicsObjectをSceneから取り出そうとすると，
            # 親クラスであるQGraphicsItem(QPixmapGraphicsItem)にダウンキャスト
            # されて返ってくるためtryが必要．
            try:
                if blockID == item.objectName():
                    return item
            except:
                pass
        return None

    def evaluateSelectedBlock(self, update=True):
        self.im_output = None

        frame = self.blocklyWebView.page().mainFrame()

        text = frame.evaluateJavaScript("Apps.getCodeFromSelectedBlock();")
        self.reflectSelectedBlockStateIntoUI()
        if text == "" or text is None:
            text = frame.evaluateJavaScript("Apps.getCodeFromWorkspace();")

        if text is None:
            return False

        xmlText = frame.evaluateJavaScript("Apps.getBlockData();")

        text = self.parseToClass(text)

        logger.debug("Generated Code: {0}".format(text))

        textHash = hashlib.md5(text.encode())
        if self.filterClassHash != textHash:
            self.filterClassHash = textHash
            try:
                exec(text, globals())
                self.filter = filterOperation(self.cv_img)
                self.filter.fgbg = self.fgbg
            except Exception as e:
                logger.debug("Block Evaluation Error: {0}".format(e))
                return False

        try:
            self.im_output = self.filter.filterFunc(self.cv_img)
        except Exception as e:
            logger.debug("Filter execution Error: {0}".format(e))
            return False

        if update:
            self.outputScene.clear()

            try:
                qimg = misc.cvMatToQImage(self.im_output)
                self.outputPixmap = QPixmap.fromImage(qimg)
            except:
                pass

            rect = QtCore.QRectF(self.outputPixmap.rect())
            self.outputScene.setSceneRect(rect)

            self.outputScene.addPixmap(self.outputPixmap)

            self.outputGraphicsView.viewport().update()
            self.outputGraphicsViewResized()

        return True

    def saveVideoFile(self, activated=False):
        self.blocklyEvaluationTimer.stop()

        if self.evaluateSelectedBlock(False):
            if self.filePath is not None:
                candidateFilePath = os.path.splitext(self.filePath)[0] + '_processed.avi'
            else:
                candidateFilePath = userDir + '_processed.avi'
            filePath, _ = QFileDialog.getSaveFileName(None, 'Save Video', candidateFilePath, "AVI files (*.avi)")

            if len(filePath) is not 0:
                logger.debug("Saving Video: {0}".format(filePath))

                self.videoPlaybackWidget.stop()

                fourcc = cv2.VideoWriter_fourcc(*'X264')
                out = cv2.VideoWriter(filePath, fourcc, self.videoPlaybackWidget.getFPS(), self.im_output.shape[1::-1])

                numFrames = self.videoPlaybackWidget.getMaxFramePos()+1
                progress = QProgressDialog("Running...", "Abort", 0, numFrames, self)
                progress.setWindowModality(Qt.WindowModal)

                currentFrameNo = self.videoPlaybackWidget.getFramePos()
                for i in range(numFrames):
                    progress.setValue(i)
                    if progress.wasCanceled():
                        break

                    ret, input_frame = self.videoPlaybackWidget.readFrame(i)
                    output_frame = self.filter.filterFunc(input_frame)
                    if len(output_frame.shape)==2:
                        output_frame = cv2.cvtColor(output_frame, cv2.COLOR_GRAY2BGR)
                    out.write(output_frame)

                out.release()

                self.videoPlaybackWidget.moveToFrame(currentFrameNo)
                progress.setValue(numFrames)


        self.blocklyEvaluationTimer.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.setWindowIcon(QIcon(':/icon/icon.ico'))
    MainWindow.setWindowTitle('UMATracker-FilterGenerator')
    MainWindow.show()
    sys.exit(app.exec_())

