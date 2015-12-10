from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsItemGroup, QGraphicsPixmapItem, QGraphicsEllipseItem, QFrame, QFileDialog, QPushButton, QGraphicsObject
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPolygonF, QColor
from PyQt5.QtCore import QPoint, QPointF, QRectF, Qt, pyqtSignal

import numpy as np
from scipy.spatial import ConvexHull

import copy


class MovablePolygonVertex(QGraphicsObject):
    geometryChange = pyqtSignal(object)

    def __init__(self, parent=None):
        super(MovablePolygonVertex, self).__init__(parent)
        self.setZValue(1000)

        self.isMousePressed = False

        self.setFlags(QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemIsFocusable |
                      QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)

        self.buttonList = []
        self.points = []
        self.setFocus(Qt.ActiveWindowFocusReason)

        self._boundingRect = QRectF()
        self._rect = QRectF()

    def setPoints(self, ps):
        self.points.clear()
        for point in ps:
            self.points.append(QPointF(*point))
        self.updateResizeHandles()

    def setRect(self):
        polygon = QPolygonF(self.points)
        rect = polygon.boundingRect()
        self._rect = rect
        self._boundingRect = rect

    def prepareGeometryChange(self):
        self.geometryChange.emit([[p.x(), p.y()] for p in self.points])
        super(MovablePolygonVertex, self).prepareGeometryChange()

    def hoverMoveEvent(self, event):
        hoverMovePos = event.scenePos()
        mouseHoverArea = None
        for item in self.buttonList:
            if item.contains(hoverMovePos):
                mouseHoverArea = item
                break
        if mouseHoverArea:
            self.setCursor(QtCore.Qt.PointingHandCursor)
            return
        self.setCursor(QtCore.Qt.SizeAllCursor)
        super(MovablePolygonVertex, self).hoverMoveEvent(event)

    def hoverEnterEvent(self, event):
        self.setCursor(QtCore.Qt.SizeAllCursor)
        super(MovablePolygonVertex, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        super(MovablePolygonVertex, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        self.isMousePressed = True
        self.mousePressedPos = event.scenePos()
        self.pressedRectPos = None
        self.originalPoints = copy.deepcopy(self.points)
        for i, item in enumerate(self.buttonList):
            if item.contains(self.mousePressedPos):
                self.pressedRectPos = i
                break
        super(MovablePolygonVertex, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.isMousePressed = False
        self.updateResizeHandles()
        self.prepareGeometryChange()
        super(MovablePolygonVertex, self).mouseReleaseEvent(event)

    def paint(self, painter, option, widget):
        self.updateResizeHandles()
        self.draw(painter, option, widget, self._rect)
        for item in self.buttonList:
            painter.drawRect(item)

    def draw(self, painter, option, widget, rect):
        return

    def boundingRect(self):
        return self._boundingRect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def mouseMoveEvent(self, event):
        mouseMovePos = event.scenePos()
        if self.isMousePressed:
            if self.pressedRectPos is None:
                for i, point in enumerate(self.points):
                    newPos = self.originalPoints[i] + (mouseMovePos - self.mousePressedPos)
                    point.setX(newPos.x())
                    point.setY(newPos.y())
            else:
                newPos = self.originalPoints[self.pressedRectPos] + (mouseMovePos - self.mousePressedPos)
                self.points[self.pressedRectPos].setX(newPos.x())
                self.points[self.pressedRectPos].setY(newPos.y())
        self.updateResizeHandles()
        self.prepareGeometryChange()

    def updateResizeHandles(self):
        self.resizeHandleSize = 4.0

        self.setRect()
        self._rect = self._rect.normalized()

        # FIXME:結構アドホック，複数のビューでシーンを表示してるときには問題が出る．
        views = self.scene().views()
        self.offset = self.resizeHandleSize * (views[0].mapToScene(1, 0).x() - views[0].mapToScene(0, 1).x())
        self._boundingRect = self._rect.adjusted(
                -self.offset*2,
                -self.offset*2,
                self.offset*2,
                self.offset*2
            )

        self.buttonList.clear()
        for point in self.points:
            rect = QRectF(
                    point.x()-self.offset,
                    point.y()-self.offset,
                    2*self.offset,
                    2*self.offset
                )
            self.buttonList.append(rect)

class MovablePolygon(MovablePolygonVertex):
    def __init__(self, parent=None):
        super(MovablePolygon, self).__init__(parent)

    def draw(self, painter, option, widget, rect):
        if len(self.points) != 0:
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 0, QtCore.Qt.DashLine))
            # hull = ConvexHull([[p.x(), p.y()] for p in self.points])
            # polygon = QPolygonF([self.points[i] for i in hull.vertices])
            polygon = QPolygonF(self.points)
            painter.drawConvexPolygon(polygon)
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.SolidLine))
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))

