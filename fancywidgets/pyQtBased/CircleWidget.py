
from PyQt4 import QtGui,QtCore


class CircleWidget(QtGui.QWidget):
    '''a simple circle - useful as indicator'''
    
    def __init__(self, parent=None, 
                 circle_size=6, 
                 pen_size=2,
                 circle_color=QtCore.Qt.red, 
                 pen_color=QtCore.Qt.darkRed,
                 antialiased=True):
        super(CircleWidget, self).__init__(parent)
        
        self.circle_size = circle_size
        self.pen_size = pen_size
        self.circle_color = circle_color
        self.pen_color = pen_color
        self.antialiased = antialiased

        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setFixedSize(QtCore.QSize(self.circle_size+self.pen_size, 
                                       self.circle_size+self.pen_size))


    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, self.antialiased)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setBrush(self.circle_color)
        painter.setPen(QtGui.QPen(self.pen_color
                                  , self.pen_size) )

        painter.drawEllipse(QtCore.QRect(-self.circle_size / 2,
                            -self.circle_size / 2,
                            self.circle_size,
                            self.circle_size))



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w= CircleWidget()
    w.setWindowTitle(w.__class__.__name__)

    w.show()
    app.exec_()