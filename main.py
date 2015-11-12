#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, six

if six.PY2:
    reload(sys)
    sys.setdefaultencoding('UTF8')

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    currentDirPath = sys._MEIPASS
    import win32api
    win32api.SetDllDirectory(sys._MEIPASS)
    win32api.SetDllDirectory(os.path.join(sys._MEIPASS, 'dll'))
elif __file__:
    currentDirPath = os.getcwd()

# currentDirPath = os.path.abspath(os.path.dirname(__file__) )
sampleDataPath = os.path.join(currentDirPath,"data")
userDir        = os.path.expanduser('~')

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

import re, hashlib, json

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QMainWindow, QDialog
from PyQt5.QtGui import QPixmap, QColor, QBrush
from PyQt5.QtCore import QRectF, QPointF, Qt

from lib.python.ui.main_window_base import Ui_MainWindowBase
from lib.python.ui.resizable_object import ResizableRect, ResizableEllipse
from lib.python.ui.background_generator_dialog import BackgroundGeneratorDialog

from lib.python import misc

import cv2
from lib.python.FilterIO.FilterIO import FilterIO
from lib.python.PythonClassGenerator.ClassTextGenerator import ClassTextGenerator

#For block evaluation, DO NOT REMOVE!#
import numpy as np
from lib.python.pycv import filters
######################################

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


class Ui_MainWindow(QMainWindow, Ui_MainWindowBase):
    def __init__(self, path):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        self.videoPlaybackInit()
        self.blocklyInit()
        self.imgInit()
        self.menuInit()
        self.menubar.setNativeMenuBar(False)
        self.selectedBlockID = None
        self.fgbg = None
        #b = RectForAreaSelection(QRectF(250, 250, 350.0, 350.0),None,self.inputGraphicsView)
        #self.inputScene.addItem(b)
        self.inputPixMapItem.mousePressEvent = self.getPixMapItemClickedPos

    def dragEnterEvent(self,event):
        event.acceptProposedAction()

    def dropEvent(self,event):
        # event.setDropAction(QtCore.Qt.MoveAction)
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

    def videoPlaybackInit(self):
        self.videoPlaybackWidget.hide()
        self.videoPlaybackWidget.frameChanged.connect(self.setFrame)

    def setFrame(self, frame):
        if frame is not None:

            self.cv_img = frame
            self.updateInputGraphicsView()

            self.evaluateSelectedBlock()

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

        self.actionCreateBackground.triggered.connect(self.createBackground)
        #self.actionTest00.triggered.connect(self.test00)

    def setRectangleParameterToBlock(self, topLeft, bottomRight):
        height, width, dim = self.cv_img.shape
        parameters = {
                    'topX': topLeft.x()/width,
                    'topY': topLeft.y()/height,
                    'bottomX': bottomRight.x()/width,
                    'bottomY': bottomRight.y()/height
                    }
        string = json.dumps({k: str(v) for k, v in parameters.items()})
        webFrame = self.blocklyWebView.page().mainFrame()
        webFrame.evaluateJavaScript("Apps.setValueToSelectedBlock({0});".format(string))

    def createBackground(self, activated=False):
        if self.videoPlaybackWidget.isOpened():
            self.videoPlaybackWidget.stop()

            bg_dialog = BackgroundGeneratorDialog(self)
            # bg_dialog.openVideoFile(filePath=self.filePath)
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

    def getPixMapItemClickedPos(self, event):
        pos = event.scenePos().toPoint()
        print(pos)

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
            self.fgbg = filterIO.getBackgroundImg()

            exec(filterIO.getFilterCode(), globals())

            blockXML = re.sub(r"[\n\r]",'', filterIO.getBlockXMLData())
            frame = self.blocklyWebView.page().mainFrame()
            frame.evaluateJavaScript("Apps.setBlockData('{0}');".format(blockXML))

    def saveFilterFile(self):
        self.blocklyEvaluationTimer.stop()
        filePath, _ = QFileDialog.getSaveFileName(None, 'Save Filter File', userDir, "Filter files (*.filter)")

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
        self.inputGraphicsView.fitInView(QtCore.QRectF(self.inputPixMap.rect()), QtCore.Qt.KeepAspectRatio)

    def outputGraphicsViewResized(self, event=None):
        self.outputGraphicsView.fitInView(self.outputScene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def parseToClass(self, text):
        additionalText = """#self.fgbg = None
if self.fgbg is not None:
    {input} = cv2.absdiff({input}, self.fgbg)
"""
#         additionalText = """#self.fgbg = None
# if self.fgbg is not None:
#     mask = self.fgbg.apply({input}, learningRate=0)
#     _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
#     {input} = cv2.bitwise_and({input}, {input}, mask=mask)
# """
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
                height, width, dim = self.cv_img.shape
                rect = QRectF(
                        float(parameters['topX'])*width,
                        float(parameters['topY'])*height,
                        float(parameters['bottomX'])*width - float(parameters['topX'])*width,
                        float(parameters['bottomY'])*height - float(parameters['topY'])*height)

                if blockType == "rectRegionSelector":
                    graphicsItem = ResizableRect()
                elif blockType == "ellipseRegionSelector":
                    graphicsItem = ResizableEllipse()
                graphicsItem.setRect(rect)

                graphicsItem.setObjectName(blockID)
                graphicsItem.geometryChange.connect(self.setRectangleParameterToBlock)
                self.inputScene.addItem(graphicsItem)

            self.updateInputGraphicsView()

        elif 'colorSelector' in blockAttributes:
            self.inputPixMapItem.mousePressEvent = self.inputPixMapItemClicked
        else:
            self.inputPixMapItem.mousePressEvent = self.getPixMapItemClickedPos

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
                self.filter.fgbg = self.fgbg
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
    MainWindow = Ui_MainWindow(currentDirPath)
    MainWindow.show()
    sys.exit(app.exec_())

