#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, we draw text in Russian azbuka.

author: Jan Bodnar
website: zetcode.com 
last edited: September 2011
"""

import sys,os,time
from PyQt4 import QtGui, QtCore


class Splash(QtGui.QWidget):
    def __init__(self,filename,time=5000,callback=lambda: None):
        super(self.__class__,self).__init__()

        self.callback=callback

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.movie = QtGui.QMovie(filename, QtCore.QByteArray())

        self.movie_screen = QtGui.QLabel(self)

        self.setFixedSize(QtGui.QPixmap(filename).size())
        rect = self.geometry()
        rect.moveCenter(QtGui.QApplication.desktop().availableGeometry().center())
        self.setGeometry(rect)


        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie_screen.setMovie(self.movie)

        self.timer = QtCore.QTimer(interval=time,parent=self)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.stop)

        self.movie.start()
        self.timer.start()


    def stop(self):
        self.timer.stop()
        self.hide()
        self.destroy()
        time.sleep(1)
        self.callback()




class Visualisation(QtGui.QMainWindow):
    
    def __init__(self,radius):
        super(self.__class__,self).__init__()

        width = 1024
        height = 640
        
        self.radius = radius
        self.dir = 0
        self.pointing = False
        self.rotation = 0
        self.crossfadeRange = (-90, 90)
        self.volumeRange = (-120, 120)

        self.setFixedSize(width,height)
        rect = self.geometry()
        rect.moveCenter(QtGui.QApplication.desktop().availableGeometry().center())
        self.setGeometry(rect)
        
        
        self.xLp=240
        self.yLp=16

        self.xVolume=0
        self.yVolume=0

        self.xCrossfade=0
        self.yCrossfade=0

        background=QtGui.QImage("resources/background.png")
        self.background=background.scaled(width,height)

        scale=self.height()/float(background.height())


        lp=QtGui.QImage("resources/platte.png")
        self.lp=lp.scaled(lp.width()*scale,lp.height()*scale)

        foreground=QtGui.QImage("resources/topLayer.png")
        self.foreground=foreground.scaled(foreground.width()*scale,foreground.height()*scale)

        pointer=QtGui.QImage("resources/hand.png")
        self.pointer=pointer.scaled(pointer.width()*scale,pointer.height()*scale)

        sliderCrossfade=QtGui.QImage("resources/slider_crossfade.png")
        self.sliderCrossfade=sliderCrossfade.scaled(sliderCrossfade.width()*scale,sliderCrossfade.height()*scale)

        sliderVolume=QtGui.QImage("resources/slider_masterVolume.png")
        self.sliderVolume=sliderVolume.scaled(sliderVolume.width()*scale,sliderVolume.height()*scale)


        self.center=(self.xLp+self.lp.width()/2,self.yLp+self.lp.height()/2)

        self.timer = QtCore.QTimer(interval=16,parent=self)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updating)
        self.timer.start()


        self.setWindowTitle('AirScratch')

    def closeEvent(self,event=None):
        os._exit(0)

    def updating(self):
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0,0,self.background)
        qp.drawImage(self.xCrossfade,self.yCrossfade,self.sliderCrossfade)
        qp.drawImage(self.xVolume,self.yVolume,self.sliderVolume)

        qp.save()
        qp.translate(self.center[0],self.center[1])
        qp.rotate(self.rotation)
        qp.translate(-self.center[0],-self.center[1])
        qp.drawImage(self.xLp,self.yLp,self.lp)
        qp.restore()

        qp.drawImage(0,0,self.foreground)
        qp.end()

    def setCursor(self, x, y):
        self.xPointer = int(round(x + self.width / 2)) - self.radius
        self.yPointer = int(round(y + self.height / 2))

    def setCrossfader(self, factor):
        dis = abs(self.crossfadeRange[1] - self.crossfadeRange[0])
        self.xCrossfade = self.crossfadeRange[0] + dis * factor

    def setVolume(self, vol):
        dis = abs(self.volumeRange[1] - self.volumeRange[0])
        self.yVolume = self.volumeRange[0] + dis * (vol / 100.)

    def setRotation(self, rot):
        self.rotation = rot



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    gui= Visualisation(200)

    sys.exit(app.exec_())

