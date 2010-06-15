#!/usr/bin/python2.5
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

class MyGfxButton(QtGui.QGraphicsItem):
   Type = QtGui.QGraphicsItem.UserType + 1
   def __init__(self, parent, text):
       QtGui.QGraphicsItem.__init__(self)
       self.txt = QtGui.QGraphicsSimpleTextItem(self)
       self.txt.setText(text)
       self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
       self.graph = parent

   def boundingRect(self):
       adjust = 2.0
       return QtCore.QRectF(-55 - adjust, -30 - adjust,113 + adjust, 63
+ adjust)

   def shape(self):
       path = QtGui.QPainterPath()
       path.addRect(-55, -30, 110, 60)
       return path

   def paint(self, painter, option, widget):
       painter.setPen(QtCore.Qt.NoPen)
       painter.setBrush(QtCore.Qt.darkGray)
       painter.drawRect(-50, -25, 100, 50)

       gradient = QtGui.QRadialGradient(-3, -3, 100)
       if option.state & QtGui.QStyle.State_Sunken:
           gradient.setCenter(3, 3)
           gradient.setFocalPoint(3, 3)
           gradient.setColorAt(1,
QtGui.QColor(QtCore.Qt.yellow).light(120))
           gradient.setColorAt(0,
QtGui.QColor(QtCore.Qt.darkYellow).light(120))
       else:
           gradient.setColorAt(0, QtCore.Qt.yellow)
           gradient.setColorAt(1, QtCore.Qt.darkYellow)

       painter.setBrush(QtGui.QBrush(gradient))
       painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
       painter.drawRect(-55, -30, 110, 60)
       font = painter.font()
       font.setBold(True)
       self.txt.setFont(font)
       metric = QtGui.QFontMetrics(font)
       txtRect = metric.boundingRect(self.txt.text())
       self.txt.setPos(txtRect.width()/-2, -txtRect.height()/2)

   def mousePressEvent(self, event):
       self.update()
       QtGui.QGraphicsItem.mousePressEvent(self, event)

   def mouseReleaseEvent(self, event):
       self.update()
       QtGui.QGraphicsItem.mouseReleaseEvent(self, event)


class MyView(QtGui.QGraphicsView):
   def __init__(self):
       QtGui.QGraphicsView.__init__(self)
       sc = QtGui.QGraphicsScene(self)
       sc.setSceneRect(-300, -300, 600, 600)
       self.setScene(sc)

       self.setBackgroundBrush(QtGui.QBrush(QtGui.QPixmap("images/cheese.jpg")))
       self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
       self.resize(400, 300)

       btn1 = MyGfxButton(self, "Menu Item 1")
       btn2 = MyGfxButton(self, "Menu Item 2")

       sc.addItem(btn1)
       btn1.setPos(0,0)

       sc.addItem(btn2)
       btn2.setPos(0,62)

       self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
       self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

def main(args):
   app = QtGui.QApplication(args)

   win = MyView()
   win.show()

   sys.exit(app.exec_())

if __name__=="__main__":
   main(sys.argv)

