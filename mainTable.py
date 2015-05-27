#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last-Updated : <2015/05/27 14:25:58 by ymnk>
from PyQt5.QtWidgets import (QApplication,QWidget,QMainWindow,QTableWidget,QTableWidgetItem,QLineEdit,QSlider,QLabel)
from PyQt5.QtWidgets import (QPushButton)
from PyQt5.QtWidgets import (QHBoxLayout,QVBoxLayout)
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
import sys,os
import numpy as np
import sqlite3

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

        self.previousButton = QPushButton("&<<")
        self.previousButton.setMaximumSize(self.previousButton.minimumSizeHint())
        self.previousButton.clicked.connect(self.frameDecrement)
        self.frameEdit = QLineEdit("0")
        self.frameEdit.setMaximumSize(QSize(100,21))
        self.frameEdit.returnPressed.connect(self.frameNEdited)
        self.nextButton = QPushButton("&>>")
        self.nextButton.setMaximumSize(self.nextButton.minimumSizeHint())
        self.nextButton.pressed.connect(self.frameIncrement)

        self.mainWidget = QWidget(self)
        self.mainLayout = QVBoxLayout(self.mainWidget)


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

        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.resize(1680,1050)
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
