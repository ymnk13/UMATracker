#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last-Updated : <2015/07/01 12:19:30 by ymnk>
from PyQt5.QtWidgets import (QApplication,QWidget,QMainWindow,QTableWidget,QTableWidgetItem,QLineEdit,QSlider,QLabel,QGraphicsWidget,QGraphicsScene,QGraphicsView,QGraphicsItem,QGraphicsEllipseItem)
from PyQt5.QtWidgets import (QPushButton)
from PyQt5.QtWidgets import (QHBoxLayout,QVBoxLayout)
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt,QVariant
from PyQt5.QtSql import QSqlTableModel,QSqlDatabase,QSqlQuery
import sys,os
import numpy as np
import sqlite3


import filePath
sys.path.append( filePath.pythonLibDirPath )
print filePath.pythonLibDirPath 
import misc

sys.path.append( os.path.join(filePath.pythonLibDirPath, 'ui') )
from trackingFixWindow import *


class Ui_fixTrackingWindow(trackingFixWindow):
    def setupUi(self,MainWindow, path):
        super(Ui_fixTrackingWindow, self).setupUi(MainWindow)
        self.databaseInit()
        self.setSliderMaximum()
        self.videoPlaybackSlider.valueChanged.connect(self.videoPlaybackSliderValueChanged)

    def videoPlaybackSliderValueChanged(self,sliderValue):
        self.model.setFilter( "frameN='{0}'".format(sliderValue))
    def setSliderMaximum(self):
        query = QSqlQuery()
        query.exec_("select max(frameN) from dates")
        query.next()
        maxFrameN = int(query.value(0))
        self.videoPlaybackSlider.setMaximum(maxFrameN)

    def databaseInit(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE");
        self.db.setDatabaseName("./data/acceptData.db");
        query = QSqlQuery()
        #query.exec_("select person where frameN == 0")
        #self.setFilter()

        if not self.db.open():
            QMessageBox.critical(None, "Cannot open database",
                                 "Unable to establish a database connection.\n"
                                 "This example needs SQLite support. Please read the Qt SQL "
                                 "driver documentation for information how to build it.\n\n"
                                 "Click Cancel to exit.",
                                 QMessageBox.Cancel)
            return False
        query = QSqlQuery()
        #query.exec_("create table person (id int primary key, firstname text, lastname text );")
        #query.exec_("insert into person values(105, 'Maria', 'Papadopoulos')");
        #query.exec_("insert into person values(106, 'Maria', 'Papadopoulos')");
        #query.exec_("select max(frameN) from dates")
        #query.next()

        
        self.model = QSqlTableModel(None,self.db)
        self.model.setTable('dates') #<= すごくたいせつ
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.setFilter( "frameN='105'" );
        self.model.select()
  
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "フレーム数")
        self.model.setHeaderData(2, Qt.Horizontal, "X座標")
        self.model.setHeaderData(3, Qt.Horizontal, "Y座標")
        self.model.setHeaderData(4, Qt.Horizontal, "固有ID")



        self.model.select()
        self.model.submitAll();
        
        self.tableView.setModel(self.model)
        self.tableView.setColumnHidden(0, True)
        self.tableView.setColumnHidden(1, True)
        self.tableView.resizeColumnsToContents()
        

def main():
    print "A"
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_fixTrackingWindow()
    ui.setupUi(MainWindow,filePath.currentDirPath)
    MainWindow.show()
    sys.exit(app.exec_())



if __name__  == "__main__":
    main()
