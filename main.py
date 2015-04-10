#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last-Updated : <2015/04/10 19:47:56 by ymnk>


from PyQt5.QtWidgets import (QApplication, QWidget, 
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton,QMainWindow,QAction,QFileDialog,QGraphicsScene,QSizePolicy)
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, QTextStream, QIODevice, QFile, QSettings, QVariant,Qt
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsView,QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap,QImage
from PyQt5 import QtWebKitWidgets
#import PyQt5.QtCore.Qt as Qt
import cv2
import sys
import os
import numpy as np

def convertQImageToMat(incomingImage):
    # http://stackoverflow.com/questions/18406149/pyqt-pyside-how-do-i-convert-qimage-into-opencvs-mat-format
    '''  Converts a QImage into an opencv MAT format  '''
    print incomingImage
    
    incomingImage = incomingImage.convertToFormat(QImage.Format_RGB32)
    #incomingImage = incomingImage.transformed(QImage.Format_RGB888)
    width = incomingImage.width()
    height = incomingImage.height()
    print width
    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr


class BrowserComp(QWidget):
    def __init__(self,parent = None,ImgComp = None,ImgOut = None):
        super(BrowserComp, self).__init__(parent)
        self.ImgObj = ImgComp
        self.ImgOut = ImgOut
        self.webView = QtWebKitWidgets.QWebView(self)
        #sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #sizePolicy.setHorizontalStretch(1)
        #sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
        self.webView.setSizePolicy(sizePolicy)

        self.webView.setObjectName("webView")
        path = os.path.abspath(os.path.dirname(__file__) )
        url = "file://{0}".format(os.path.join(path,"lib","blicks","index.html"))
        url = "file://{0}".format(os.path.join(path,"lib","blockly","index2.html"))
        
        qurl = QUrl(url)
        self.webView.load(qurl)
        # http://nullege.com/codes/search/PyQt5.QtWebKitWidgets.QWebView.loadFinished.connect
        self.webView.loadFinished.connect(self.on_webView_loadFinished)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.webView)


        self.button = QPushButton("&Execute")
        self.button.clicked.connect(self.executeScript)

        #self.button_canny = QPushButton("&Canny")
        #self.button_canny.clicked.connect(self.executeCanny)


        self.mainLayout.addWidget(self.button)
        #self.mainLayout.addWidget(self.button_canny)
        self.setLayout(self.mainLayout)
        
    def executeCanny(self):
        im_input = convertQImageToMat(self.ImgObj.pic_Item.pixmap().toImage())
        im_gray =cv2.cvtColor(im_input,cv2.COLOR_BGR2GRAY)
        im_edges = cv2.Canny(im_gray,100,200)
        im_out = im_edges
        self.eveluate(im_out)

    def eveluate(self,im_out):
        if hasattr(im_out,"shape"):
            if len(im_out.shape)<=2:
                height, width = im_out.shape
                dim = im_out.size/(height*width)
            else:
                height, width,dim = im_out.shape
                dim = 3
        else:
            im_out = im_out[1]
            height = len(im_out)
            width = len(im_out[0])
            dim = 1

        #print im_out.dtype,
        bytesPerLine = dim * width
        #Opencv（numpy）画像をQtのQImageに変換
        image = QImage(im_out.data, width, height, bytesPerLine,QImage.Format_Indexed8)#QImage.Format_RGB888)
        #print im_out.shape,im_out
        #image2 = image.scaled(width*0.75, height*0.75,Qt.KeepAspectRatio)
        qimage = QPixmap.fromImage(image)
        
        qimage = qimage.scaled(width*0.75, height*0.75,Qt.KeepAspectRatio)
        pic_Item = QGraphicsPixmapItem(qimage)
        
        
        #画像を描画
        self.ImgOut.scene.addItem(pic_Item)
        #cv2.imshow("",im_edges)
        #cv2.waitKey(0)

    def executeScript(self):
        frame = self.webView.page().mainFrame()
        self.processSequence(frame)
        getJS = """
function showCode() {
	// Generate JavaScript code and display it.
	Blockly.Python.INFINITE_LOOP_TRAP = null;
	var code = Blockly.Python.workspaceToCode();
    return code;
}
showCode();
"""
        text = frame.evaluateJavaScript(getJS)
        #script = frame.findFirstElement('#SCRIPT')
        #text = script.toPlainText()
        print text
        im_input = convertQImageToMat(self.ImgObj.pic_Item.pixmap().toImage())
        #text = "im_output = cv2.cvtColor((im_input),cv2.COLOR_BGR2GRAY)"
        try:
            exec(text)
        except Exception as e:
            print e
            print "Error Code"
        """
        print im_input.dtype,im_input.shape
        im_gray =cv2.cvtColor(im_input,cv2.COLOR_BGR2GRAY)
        print im_gray.dtype,im_gray.shape
        im_masked = None

        width,height,dim = im_input.shape
        im_mask = np.ones((width,height), dtype=np.uint8)
        im_mask *= 255
        cv2.circle(im_mask,(190,10), radius = 100, color = 0,thickness = -1)
        im_masked = im_mask
        im_output = im_masked

        print im_output.shape
        """
        self.eveluate(im_output)

        

    def on_webView_loadFinished(self):
        # Begin document inspection.
        frame = self.webView.page().mainFrame()
        self.processSequence(frame)

    def processSequence(self, frame):
        #print frame.toHtml()
        buttonExecute = frame.findFirstElement('#execute')
        script = frame.findFirstElement('#SCRIPT')
        print buttonExecute.attribute('value')

        
"""
class MainWindow(QWidget):
    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.calcButton = QPushButton("&Calc")
        self.browser = BrowserComp(self)
        #

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.calcButton)
        self.mainLayout.addWidget(self.browser)
        self.setLayout(self.mainLayout)
"""

class Graphics(QGraphicsView):
    def __init__(self):
        super(Graphics, self).__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
    def read(self,fn):
        self.fn = fn
        self.pic_Item = QGraphicsPixmapItem(QPixmap(fn))
        self.scene.addItem(self.pic_Item)


              
class GraphicsWidget(QWidget):
    def __init__(self):
        super(GraphicsWidget, self).__init__()
        self.graphics = Graphics()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.graphics)
        self.setLayout(self.mainLayout)

    def read(self,fn):
        self.graphics.read(fn)
  

class MainWindow(QMainWindow):
    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Main Window Framework")
        self.file_menu = self.menuBar().addMenu("&File")
        #self.file_menu.addMenu("New...")
        

        # Open Action
        openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.openFile)
        
        # Close Menu
        closeAction = QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Notepad')
        closeAction.triggered.connect(self.close)

        self.file_menu.addAction(openAction)
        self.file_menu.addAction(closeAction)
        
        #QGraphicsScene
        self.graphicsIn = GraphicsWidget()
        self.graphicsOut = GraphicsWidget()
        self.browser = BrowserComp(self,self.graphicsIn.graphics,self.graphicsOut.graphics)
        path = os.path.abspath(os.path.dirname(__file__) )
        img_fn = os.path.join(path,"data","frame1894.png")
        self.graphicsIn.read(img_fn)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.browser)
        self.mainVLayout = QVBoxLayout()
        self.mainVLayout.addWidget(self.graphicsIn)
        self.mainVLayout.addWidget(self.graphicsOut)

        self.mainLayout.addLayout(self.mainVLayout)
        mainWidget = QWidget()
        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)
        self.resize(1680,1050)
        
    def openFile(self):
        #path = os.getenv('HOME')
        path = os.path.dirname(__file__) 
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File',path)
        self.graphics.read(filename)


def main():
    print Qt
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    
    
    sys.exit(app.exec_())


if __name__  == "__main__":
    main()
