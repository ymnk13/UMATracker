#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsObject

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import Qt
import copy
from PyQt5.QtCore import pyqtSignal


class RectForAreaSelection(QGraphicsObject):
    geometryChange = pyqtSignal('QPointF', 'QPointF')

    def __init__(self, rect, parent=None, view=None):
        super(QGraphicsObject, self).__init__()
        self._view = view
        self._rect = rect
        self._boundingRect = rect

        self.mouseIsPressed = None
        #
        self.setFlags(QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemIsFocusable |
                      QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        #
        self._buttonList = {}
        self.setFocus(Qt.ActiveWindowFocusReason)
        self.updateResizeHandles()

    def prepareGeometryChange(self):
        self.geometryChange.emit(self._rect.topLeft(),
                                 self._rect.bottomRight())
        QGraphicsObject.prepareGeometryChange(self)

    def hoverMoveEvent(self, event):
        hoverMovePos = event.scenePos()
        mouseHoverArea = None
        for item in self._buttonList:
            if self._buttonList[item].contains(hoverMovePos):
                mouseHoverArea = item
                break
        if mouseHoverArea:
            self.setCursor(QtCore.Qt.PointingHandCursor)
            return
        self.setCursor(QtCore.Qt.SizeAllCursor)
        QGraphicsObject.hoverMoveEvent(self, event)

    def hoverEnterEvent(self, event):
        self.setCursor(QtCore.Qt.SizeAllCursor)
        QGraphicsObject.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        QGraphicsObject.hoverLeaveEvent(self, event)

    def mousePressEvent(self, event):
        self.mouseIsPressed = True
        self.mousePressPos = event.scenePos()
        self.rectPress = copy.deepcopy(self._rect)
        self.mousePressArea = None
        for item in self._buttonList:
            if self._buttonList[item].contains(self.mousePressPos):
                self.mousePressArea = item
                break
        QGraphicsObject.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.mouseIsPressed = False
        self.updateResizeHandles()
        self.prepareGeometryChange()
        QGraphicsObject.mouseReleaseEvent(self, event)

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 0, QtCore.Qt.DashLine))
        painter.drawRect(self._rect)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        for item in self._buttonList:
            painter.drawRect(self._buttonList[item])

    def boundingRect(self):
        return self._boundingRect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def mouseMoveEvent(self, event):
        mouseMovePos = event.scenePos()
        if self.mouseIsPressed:
            if self.mousePressArea == 'topRect':
                self._rect.setTop(
                        self.rectPress.y() - (self.mousePressPos.y() - mouseMovePos.y())
                        )
            elif self.mousePressArea == 'bottomRect':
                self._rect.setBottom(
                        self.rectPress.bottom() - (self.mousePressPos.y() - mouseMovePos.y())
                        )
            elif self.mousePressArea == 'leftRect':
                self._rect.setLeft(
                        self.rectPress.left() - (self.mousePressPos.x() - mouseMovePos.x())
                        )
            elif self.mousePressArea == 'rightRect':
                self._rect.setRight(
                        self.rectPress.right() - (self.mousePressPos.x() - mouseMovePos.x())
                        )
            elif self.mousePressArea == 'topleftRect':
                self._rect.setTopLeft(
                        self.rectPress.topLeft() - (self.mousePressPos - mouseMovePos)
                        )
            elif self.mousePressArea == 'toprightRect':
                self._rect.setTopRight(
                        self.rectPress.topRight() - (self.mousePressPos - mouseMovePos)
                        )
            elif self.mousePressArea == 'bottomleftRect':
                self._rect.setBottomLeft(
                        self.rectPress.bottomLeft() - (self.mousePressPos - mouseMovePos)
                        )
            elif self.mousePressArea == 'bottomrightRect':
                self._rect.setBottomRight(
                        self.rectPress.bottomRight() - (self.mousePressPos - mouseMovePos)
                        )
            else:
                self._rect.moveCenter(
                        self.rectPress.center() - (self.mousePressPos - mouseMovePos)
                        )
        self.updateResizeHandles()
        self.prepareGeometryChange()

    def updateResizeHandles(self):
        self.resizeHandleSize = 4.0
        self.offset = self.resizeHandleSize * (self._view.mapToScene(1, 0).x() - self._view.mapToScene(0, 1).x())
        self._boundingRect = self._rect.adjusted(
                -self.offset*2,
                -self.offset*2,
                self.offset*2,
                self.offset*2
            )
        self._buttonList["topRect"] = QRectF(
                self._rect.center().x(),
                self._boundingRect.topLeft().y()+self.offset,
                2*self.offset,
                2*self.offset
            )
        self._buttonList["bottomRect"] = QRectF(
                self._rect.center().x(),
                self._rect.bottom()-self.offset,
                2*self.offset,
                2*self.offset
            )
        self._buttonList["leftRect"] = QRectF(
                self._rect.x()-self.offset,
                self._rect.center().y()-self.offset,
                2*self.offset,
                2*self.offset
            )
        self._buttonList["rightRect"] = QRectF(
                self._rect.right()-self.offset,
                self._rect.center().y()-self.offset,
                2*self.offset,
                2*self.offset
            )
        self._buttonList["topleftRect"] = QRectF(
                self._boundingRect.topLeft().x()+self.offset,
                self._boundingRect.topLeft().y()+self.offset,
                2*self.offset,
                2*self.offset
            )
        self._buttonList["toprightRect"] = QRectF(
                self._boundingRect.topRight().x()-3*self.offset,
                self._boundingRect.topRight().y()+self.offset,
                2*self.offset,
                2*self.offset
            )
        self._buttonList["bottomleftRect"] = QRectF(
                self._boundingRect.bottomLeft().x()+self.offset,
                self._boundingRect.bottomLeft().y()-3*self.offset,
                2*self.offset,
                2*self.offset
            )
        self._buttonList["bottomrightRect"] = QRectF(
                self._boundingRect.bottomRight().x()-self.offset*3,
                self._boundingRect.bottomRight().y()-self.offset*3,
                2*self.offset,
                2*self.offset
            )


def main():
    pass

if __name__ == "__main__":
    main()
