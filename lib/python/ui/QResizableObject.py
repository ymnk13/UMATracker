#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui

from QUserDefinedBaseObject import QResizableGraphicsObject


class QResizableRect(QResizableGraphicsObject):
    def __init__(self, rect, parent=None, view=None):
        super(QResizableRect, self).__init__(rect, parent, view)

    def draw(self, painter, option, widget, rect):
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 0, QtCore.Qt.DashLine))
        painter.drawRect(rect)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))


class QResizableEllipse(QResizableGraphicsObject):
    def __init__(self, rect, parent=None, view=None):
        super(QResizableEllipse, self).__init__(rect, parent, view)

    def draw(self, painter, option, widget, rect):
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 0, QtCore.Qt.DashLine))
        painter.drawEllipse(rect)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))


def main():
    pass

if __name__ == "__main__":
    main()
