from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.uix.image import Image
from kivy.config import Config

from kivy.uix.widget import Widget

import os,time

class Visualisation(App):

    def __init__(self,radius):
        super(self.__class__,self).__init__()
        self.width = 1024
        self.height = 640

        Config.set('graphics', 'width', self.width)
        Config.set('graphics', 'height', self.height)
        Config.set("graphics","resizable",0)


        self.radius = radius
        self.dir = 0
        self.pointing = False
        self.rotation = 0
        self.crossfadeRange = (-90, 90)
        self.volumeRange = (-120, 120)

        # rect = self.geometry()
        # rect.moveCenter(QtGui.QApplication.desktop().availableGeometry().center())
        # self.setGeometry(rect)
        # 
        
        self.xLp=240
        self.yLp=16
        self.widthLp=608
        self.heightLp=608

        self.sliderVolume=None
        self.sliderCrossfade=None
        self.mainWidget=None
        self.lpScatter=None
        self.pointer=None


    def build(self):


        background=Image(source="resources/background.png",size=(self.width,self.height))
        foreground=Image(source="resources/topLayer.png",size=(self.width,self.height))
        lp=Image(source="resources/platte.png",size=(self.widthLp,self.heightLp))

        self.pointer=Image(source="resources/hand.png")
        self.sliderCrossfade=Image(source="resources/slider_crossfade.png",size=(self.width,self.height))
        self.sliderVolume=Image(source="resources/slider_masterVolume.png",size=(self.width,self.height))

        self.mainWidget = Widget(size=(self.width, self.height))

        self.lpScatter = Scatter(pos=(self.xLp,self.yLp),size=(self.widthLp,self.heightLp),size_hint=(None,None))
        self.lpScatter.add_widget(lp)

        self.pointer.opacity=0


        self.mainWidget.add_widget(background)
        self.mainWidget.add_widget(self.sliderCrossfade)
        self.mainWidget.add_widget(self.sliderVolume)
        self.mainWidget.add_widget(self.lpScatter)
        self.mainWidget.add_widget(foreground)
        self.mainWidget.add_widget(self.pointer)

        return self.mainWidget



    def on_stop(self,event=None):
        os._exit(0)


    def activateCursor(self, x, y):
        self.pointer.size=(int(round(x +self.width-self.radius)),int(round(y +self.height)))
        self.pointer.opacity=1

    def deactivateCursor(self):
        self.pointer.opacity=0


    def setCrossfader(self, factor):
        dis = abs(self.crossfadeRange[1] - self.crossfadeRange[0])
        self.sliderCrossfade.x= self.crossfadeRange[0] + dis * factor

    def setVolume(self, vol):
        dis = abs(self.volumeRange[1] - self.volumeRange[0])
        self.sliderVolume.y= self.volumeRange[0] + dis * (vol / 100.)

    def setRotation(self, rot):
        self.lpScatter.rotation=-rot


    def mouseMoveEvent(self, event):
        if self.controller:
            self.controller.on_frame(event)




if __name__ == '__main__':
    Visualisation(100).run()

