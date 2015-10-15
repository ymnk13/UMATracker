#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsItem
import copy

from .QUserDefinedBaseObject import QResizableGraphicsObject

class QResizableRect(QResizableGraphicsObject):
    def __init__(self, parent=None):
        super(QResizableRect, self).__init__(parent)

    def draw(self, painter, option, widget, rect):
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 0, QtCore.Qt.DashLine))
        painter.drawRect(rect)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))


class QResizableEllipse(QResizableGraphicsObject):
    def __init__(self, parent=None):
        super(QResizableEllipse, self).__init__(parent)

    def draw(self, painter, option, widget, rect):
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 0, QtCore.Qt.DashLine))
        painter.drawEllipse(rect)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))


def main():
    pass

if __name__ == "__main__":
    main()
