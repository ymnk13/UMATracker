#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last-Updated : <2015/05/27 19:12:34 by ymnk>
from PyQt5.QtWidgets import (QApplication,QWidget,QMainWindow,QTableWidget,QTableWidgetItem,QLineEdit,QSlider,QLabel,QGraphicsWidget,QGraphicsScene,QGraphicsView,QGraphicsItem,QGraphicsEllipseItem)
from PyQt5.QtWidgets import (QPushButton)
from PyQt5.QtWidgets import (QHBoxLayout,QVBoxLayout)
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
import sys,os
import numpy as np
import sqlite3

class CircleItem(QGraphicsEllipseItem):
    def __init__(self,x,y,width,height,pen,parent = None):
        super(QGraphicsEllipseItem, self).__init__(x,y,width,height)
        #self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlags(  self.flags()                            |
                        QGraphicsItem.ItemIsSelectable          |
                        QGraphicsItem.ItemIsMovable             |
                        QGraphicsItem.ItemIsFocusable           |
                        QGraphicsItem.ItemSendsScenePositionChanges )
        
    def paint(self,painter,option = None,widget = None):
        painter.setBrush(Qt.red)
        painter.drawEllipse(self.rect())
    def itemChange(self, change, variant):
        super(CircleItem, self).itemChange(change, variant)
        if change == QGraphicsItem.ItemPositionChange:
            #self.setParentItem(None)
            None
        return QGraphicsItem.itemChange(self, change, variant)

 
class SlideController(QVBoxLayout):
    def __init__(self,maxFrame,parent = None):
        super(QVBoxLayout, self).__init__(parent)
        self.previousButton = QPushButton("&<<")
        self.previousButton.setMaximumSize(self.previousButton.minimumSizeHint())
        self.frameSlider = QSlider(Qt.Horizontal)
        self.frameSlider.setRange(1,maxFrame)
        self.frameSlider.setSingleStep(1)
        #self.frameSlider.setMaximumSize(QSize(100,21))
        
        self.nextButton = QPushButton("&>>")
        self.nextButton.setMaximumSize(self.nextButton.minimumSizeHint())

        self.top = QHBoxLayout()
        self.frameLabel = QLabel("frame = ")
        self.top.addWidget(self.frameLabel)

        self.bottom = QHBoxLayout()
        self.bottom.addWidget(self.previousButton)
        self.bottom.addWidget(self.frameSlider)
        self.bottom.addWidget(self.nextButton)
        self.addLayout(self.top)
        self.addLayout(self.bottom)


class FrameController(QHBoxLayout):
    def __init__(self,parent = None):
        super(QHBoxLayout, self).__init__(parent)
        self.previousButton = QPushButton("&<<")
        self.previousButton.setMaximumSize(self.previousButton.minimumSizeHint())
        #self.previousButton.clicked.connect(self.frameDecrement)
        self.frameEdit = QLineEdit("0")
        self.frameEdit.setMaximumSize(QSize(100,21))
        #self.frameEdit.returnPressed.connect(self.frameNEdited)
        self.nextButton = QPushButton("&>>")
        self.nextButton.setMaximumSize(self.nextButton.minimumSizeHint())
        #self.nextButton.pressed.connect(self.frameIncrement)
        self.addWidget(self.previousButton)
        self.addWidget(self.frameEdit)
        self.addWidget(self.nextButton)
        

class MainWindow(QMainWindow):
    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.left = TableContents(self)
        #self.right = TableContents()#
        self.right = ImageContents(self)
        self.mainLayout = QHBoxLayout()
        
        
        self.mainLayout.addWidget(self.left)
        self.mainLayout.addWidget(self.right)
        self.setLayout(self.mainLayout)

        mainWidget = QWidget(self)
        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)
        self.resize(1680,1050)

class ImageContents(QWidget):
    def __init__(self,parent = None):
        super(QWidget, self).__init__(parent)
        self.button0 = QPushButton("&<<")
        self.button1 = QPushButton("&<<")
        #self.graphics = QGraphicsWidget()
        self.graphics = QGraphicsView()
        #self.graphics.resize(1920,1028)

        self.scene = QGraphicsScene(self)
        blackpen = Qt.black
        ellipse0 = self.scene.addEllipse(0,0,50,50,blackpen,blackpen)
        ellipse1 = self.scene.addEllipse(1024,1028,100,100,blackpen,blackpen)
        self.scene.addItem(CircleItem(60,60,60,60,Qt.black))
        ellipse0.setFlag(QGraphicsItem.ItemIsMovable)
        ellipse1.setFlag(QGraphicsItem.ItemIsMovable)
        self.graphics.setScene(self.scene)
        #self.graphics.scale(2000, 2000)
        print self.scene.width()
        self.topLayout = QVBoxLayout()
        self.topLayout.addWidget(self.button0)
        self.topLayout.addWidget(self.graphics)

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.button1)
        self.setLayout(self.mainLayout)


class TableContents(QWidget):
    def __init__(self,parent = None):
        super(QWidget, self).__init__(parent)
        self.conn = sqlite3.connect(os.path.abspath('./data/acceptData.db'))
        cur = self.conn.cursor()
        cur.execute("""SELECT DogTag,x,y FROM dates where frameN=1;""")

        self.patientTable = QTableWidget()
        self.patientTable.setRowCount(7)
        self.patientTable.setColumnCount(3)
        for i,item in enumerate(["個体番号","x","y"]):
            self.patientTable.setHorizontalHeaderItem(i,QTableWidgetItem(item))
        self.frameN = 0
        self.viewData(self.frameN)


        #self.mainWidget = QWidget(self)
        self.mainLayout = QVBoxLayout(self)


        # Button+Editor Version
        self.LeftLayout = QVBoxLayout()
        self.frameController = FrameController()
        self.frameController.previousButton.clicked.connect(self.frameDecrement)
        self.frameController.frameEdit.returnPressed.connect(self.frameNEdited)
        self.frameController.nextButton.pressed.connect(self.frameIncrement)

        # Slide Version
        self.slideController = SlideController(1000)
        self.slideController.previousButton.clicked.connect(self.frameDecrement)
        self.slideController.nextButton.pressed.connect(self.frameIncrement)

        self.mainLayout.addLayout(self.frameController)
        self.mainLayout.addLayout(self.slideController)
        self.mainLayout.addWidget(self.patientTable)

        #self.mainLayout.addLayout(self.LeftLayout)
        #self.mainLayout.addWidget(self.testButton)

        self.setLayout(self.mainLayout)
        #self.setCentralWidget(self.mainWidget)

        #

    def frameNEdited(self):
        text = self.frameEdit.displayText()
        if not text.isdigit():
            return
        self.frameN = int(text)
        self.viewData(self.frameN)

    def frameDecrement(self):
        if self.frameN < 0:
            return
        self.frameN-=1
        self.viewData(self.frameN)

    def frameIncrement(self):
        self.frameN+=1
        self.viewData(self.frameN)
        self.frameEdit.setText(str(self.frameN))

    def viewData(self,n):
        cur = self.conn.cursor()
        cur.execute("SELECT DogTag,x,y FROM dates where frameN={0};".format(n))
        self.patientTable.clearContents()
        row = 0
        while True:
            form = cur.fetchone()
            if form == None:
                break
            for column,item in enumerate(form):
                self.patientTable.setItem(row, column, QTableWidgetItem(str(item)))
            row+=1

        

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())

if __name__  == "__main__":
    main()
