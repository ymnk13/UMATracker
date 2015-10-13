#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, six

if six.PY2:
    reload(sys)
    sys.setdefaultencoding('UTF8')

# def tracefunc(frame, event, arg, indent=[0]):
#     if event == "call":
#         indent[0] += 2
#         if indent[0] < 10:
#             print("-" * indent[0] + "> call function", frame.f_code.co_name)
#     elif event == "return":
#         if indent[0] < 10:
#             print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
#         indent[0] -= 2
#     return tracefunc
# sys.settrace(tracefunc)

import os, re, hashlib, json

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QFileDialog
from PyQt5.QtGui import QPixmap, QColor, QBrush
from PyQt5.QtCore import QRectF, QPointF

from lib.python.ui.MainWindowBase import Ui_MainWindowBase
from lib.python.ui.QResizableObject import QResizableRect, QResizableEllipse

from lib.python import misc

import cv2
from lib.python.FilterIO.FilterIO import FilterIO
from lib.python.PythonClassGenerator.ClassTextGenerator import ClassTextGenerator

#For block evaluation, DO NOT REMOVE!#
import numpy as np
from lib.python.pycv import filters
######################################


currentDirPath = os.path.abspath(os.path.dirname(__file__) )
sampleDataPath = os.path.join(currentDirPath,"data")
userDir        = os.path.expanduser('~')

if six.PY2:
    import urllib
    blocklyURL = "file:" + urllib.pathname2url(os.path.join(currentDirPath,"lib","editor","index.html"))
elif six.PY3:
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


class Ui_MainWindow(Ui_MainWindowBase):
    def setupUi(self, MainWindow, path):
        super(Ui_MainWindow, self).setupUi(MainWindow)

        self.videoPlaybackInit()
        self.blocklyInit()
        self.imgInit()
        self.menuInit()
        self.menubar.setNativeMenuBar(False)
        MainWindow.closeEvent = self.closeEvent
        MainWindow.dragEnterEvent = self.dragEnterEvent
        MainWindow.dropEvent = self.dropEvent
        self.selectedBlockID = None
        #b = RectForAreaSelection(QRectF(250, 250, 350.0, 350.0),None,self.inputGraphicsView)
        #self.inputScene.addItem(b)
        self.sceneObjectInfo = {}

    def dragEnterEvent(self,event):
        event.accept()

    def dropEvent(self,event):
        event.setDropAction(QtCore.Qt.MoveAction)
        mime = event.mimeData()
        if mime.hasUrls():
            urls = mime.urls()
            if len(urls) > 0:
                #self.dragFile.emit()
                self.processDropedFile(urls[0].toLocalFile())
            event.accept()
        else:
            event.ignore()

    def closeEvent(self,event):
        pass

    def processDropedFile(self,filePath):
        root,ext = os.path.splitext(filePath)
        if ext == ".filter":
            # Read Filter
            self.openFilterFile(filePath=filePath)
        elif ext.lower() in [".avi",".mpg",".mts",".mp4"]:
            # Read Video
            self.openVideoFile(filePath=filePath)
        elif ext.lower() in [".png",".bmp",".jpg",".jpeg"]:
            self.openImageFile(filePath=filePath)

    def videoPlaybackInit(self):
        self.videoPlaybackWidget.hide()
        self.videoPlaybackWidget.frameChanged.connect(self.setFrame)

    def getSceneObjectInfo(self):
        for item in self.inputScene.items():
            if isinstance(item,QGraphicsPixmapItem):
                continue
            try:
                blockID = item.objectName()

                self.sceneObjectInfo[blockID]["topLeftX"] = item._rect.topLeft().x()
                self.sceneObjectInfo[blockID]["topLeftY"] = item._rect.topLeft().y()
                self.sceneObjectInfo[blockID]["bottomRightX"] = item._rect.bottomRight().x()
                self.sceneObjectInfo[blockID]["bottomRightY"] = item._rect.bottomRight().y()
            except:
                pass

    def setSceneObjectInfo(self):
        for item in self.inputScene.items():
            if isinstance(item,QGraphicsPixmapItem):
                continue
            try:
                pos = self.sceneObjectInfo[item.objectName()]
                item._rect.setTopLeft(QPointF(pos["topLeftX"],pos["topLeftY"]))
                item._rect.setBottomRight(QPointF(pos["bottomRightX"],pos["bottomRightY"]))
            except:
                pass

    def setFrame(self, frame):
        if frame is not None:

            self.getSceneObjectInfo()
            self.cv_img = frame
            self.updateInputGraphicsView()

            self.evaluateSelectedBlock()
            self.setSceneObjectInfo()

    def blocklyInit(self):
        self.blocklyWebView.setUrl(QtCore.QUrl(blocklyURL))

        self.blocklyEvaluationTimer = QtCore.QTimer(parent=self.blocklyWebView)
        self.blocklyEvaluationTimer.setInterval(1*100)
        self.blocklyEvaluationTimer.timeout.connect(self.evaluateSelectedBlock)
        self.blocklyEvaluationTimer.start()

        self.filterClassHash = None
        self.filter = None

    def imgInit(self):
        self.filePath = os.path.join(sampleDataPath,"color_filter_test.png")
        self.cv_img = cv2.imread(os.path.join(sampleDataPath,"color_filter_test.png"))

        self.inputScene = QGraphicsScene()
        self.inputGraphicsView.setScene(self.inputScene)
        self.inputGraphicsView.resizeEvent = self.inputGraphicsViewResized

        #self.inputScene.mousePressEvent = None

        self.outputScene = QGraphicsScene()
        self.outputGraphicsView.setScene(self.outputScene)
        self.outputGraphicsView.resizeEvent = self.outputGraphicsViewResized


        qimg = misc.cvMatToQImage(self.cv_img)
        self.inputPixMap = QPixmap.fromImage(qimg)
        self.inputPixMapItem = QGraphicsPixmapItem(self.inputPixMap)
        self.inputScene.addItem(self.inputPixMapItem)

    def menuInit(self):
        self.actionOpenVideo.triggered.connect(self.openVideoFile)
        self.actionOpenImage.triggered.connect(self.openImageFile)

        self.actionSaveFilterData.triggered.connect(self.saveFilterFile)
        self.actionOpenFilterData.triggered.connect(self.openFilterFile)
        #self.actionTest00.triggered.connect(self.test00)

    def setRectangleParameterToBlock(self,topLeft,bottomRight):
        parameters = {
                    'topX': topLeft.x(),
                    'topY': topLeft.y(),
                    'bottomX': bottomRight.x(),
                    'bottomY': bottomRight.y()
                    }
        string = json.dumps({k: str(int(v)) for k, v in parameters.items()})
        webFrame = self.blocklyWebView.page().mainFrame()
        webFrame.evaluateJavaScript("Apps.setValueToSelectedBlock({0});".format(string))

    def openVideoFile(self, activated=False, filePath = None):
        if filePath is None:
            filePath, _ = QFileDialog.getOpenFileName(None, 'Open Video File', userDir)

        if len(filePath) is not 0:
            self.filePath = filePath

            self.videoPlaybackWidget.show()
            self.videoPlaybackWidget.openVideo(filePath)

            self.filterClassHash = None


    def openImageFile(self, activated=False, filePath = None):
        if filePath == None:
            filePath, _ = QFileDialog.getOpenFileName(None, 'Open Image File', userDir)

        if len(filePath) is not 0:
            self.filePath = filePath
            self.cv_img = cv2.imread(filePath)
            self.videoPlaybackWidget.hide()

            self.updateInputGraphicsView()
            self.releaseVideoCapture()

            # Initialize Filter when opening new file.
            self.filterClassHash = None

    def updateInputGraphicsView(self):
        # self.inputScene.clear()
        self.inputScene.removeItem(self.inputPixMapItem)
        qimg = misc.cvMatToQImage(self.cv_img)
        self.inputPixMap = QPixmap.fromImage(qimg)

        rect = QtCore.QRectF(self.inputPixMap.rect())
        self.inputScene.setSceneRect(rect)
        self.outputScene.setSceneRect(rect)

        self.inputPixMapItem = QGraphicsPixmapItem(self.inputPixMap)
        # self.inputScene.setBackgroundBrush(QBrush(self.inputPixMap))
        self.inputScene.addItem(self.inputPixMapItem)

        self.inputGraphicsView.viewport().update()
        self.inputGraphicsViewResized()

    def inputPixMapItemClicked(self, event):
        pos = event.scenePos().toPoint()

        img = self.inputPixMap.toImage()
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

            exec(filterIO.getFilterCode(), globals())

            blockXML = re.sub(r"[\n\r]",'', filterIO.getBlockXMLData())
            frame = self.blocklyWebView.page().mainFrame()
            frame.evaluateJavaScript("Apps.setBlockData('{0}');".format(blockXML))

    def saveFilterFile(self):
        filePath, _ = QFileDialog.getSaveFileName(None, 'Save Filter File', userDir, "Filter files (*.filter)")

        if len(filePath) is not 0:
            logger.debug("Saving Filter file: {0}".format(filePath))

            frame = self.blocklyWebView.page().mainFrame()

            filterIO = FilterIO()
            filterIO.setBlockXMLData(frame.evaluateJavaScript("Apps.getBlockData();"))

            filterClassText = self.parseToClass(frame.evaluateJavaScript("Apps.getCodeFromWorkspace();"))
            filterIO.setFilterCode(filterClassText)
            filterIO.save(filePath)

    def inputGraphicsViewResized(self, event=None):
        self.inputGraphicsView.fitInView(QtCore.QRectF(self.inputPixMap.rect()), QtCore.Qt.KeepAspectRatio)

    def outputGraphicsViewResized(self, event=None):
        self.outputGraphicsView.fitInView(self.outputScene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def parseToClass(self, text):
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

    def startUIBySelectedBlock(self):
        webFrame = self.blocklyWebView.page().mainFrame()

        data = webFrame.evaluateJavaScript("Apps.getBlockTypeFromSelectedBlock();")
        if data is None:
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
                if blockID not in self.sceneObjectInfo:
                    self.sceneObjectInfo[blockID] = {}
                rect = QRectF(
                        int(parameters['topX']),
                        int(parameters['topY']),
                        int(parameters['bottomX']),
                        int(parameters['bottomY']))
                # print(rect)

                if blockType == "rectRegionSelector":
                    graphicsItem = QResizableRect(rect, None, self.inputGraphicsView)
                elif blockType == "ellipseRegionSelector":
                    graphicsItem = QResizableEllipse(rect, None, self.inputGraphicsView)

                graphicsItem.setObjectName(blockID)
                graphicsItem.geometryChange.connect(self.setRectangleParameterToBlock)
                self.inputScene.addItem(graphicsItem)

            self.updateInputGraphicsView()

        elif 'colorSelector' in blockAttributes:
            self.inputPixMapItem.mousePressEvent = self.inputPixMapItemClicked

    def resetSceneAction(self, blockID):
        graphicsItem = self.getGrphicsItemFromInputScene(blockID)
        if graphicsItem is not None:
            graphicsItem.hide()
        self.inputPixMapItem.mousePressEvent = QGraphicsPixmapItem(self.inputPixMapItem).mousePressEvent

    def getGrphicsItemFromInputScene(self, blockID):
        try:
            int(blockID)
        except:
            return None

        for item in self.inputScene.items():
            #QGraphicsObjectをSceneから取り出そうとすると，
            #親クラスであるQGraphicsItem(QPixmapGraphicsItem)にダウンキャスト
            #されて返ってくるためtryが必要．
            try:
                if blockID == item.objectName():
                    return item
            except:
                pass
        return None

    def evaluateSelectedBlock(self):
        im_output = None

        frame = self.blocklyWebView.page().mainFrame()

        text = frame.evaluateJavaScript("Apps.getCodeFromSelectedBlock();")
        self.startUIBySelectedBlock()
        if text == "" or text is None:
            text = frame.evaluateJavaScript("Apps.getCodeFromWorkspace();")

        # print(text)

        if text is None:
            return False

        xmlText = frame.evaluateJavaScript("Apps.getBlockData();")
        text = self.parseToClass(text)

        logger.debug("Generated Code: {0}".format(text))

        # TODO: あまりにも大きいイメージは縮小しないと処理がなかなか終わらない
        #       ので，そうしたほうがいい．

        textHash = hashlib.md5(text.encode())
        if self.filterClassHash != textHash:
            self.filterClassHash = textHash
            try:
                exec(text, globals())
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow,currentDirPath)
    MainWindow.show()
    sys.exit(app.exec_())

