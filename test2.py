from threading import Thread
from LPSimulator import LP
from test import Visualisation
from AngleLeapController import LeapController
from AudioController import AudioController
import time,sys

from PyQt4 import QtGui




class Controller(Thread):
    def __init__(self, baseFilePath, scratchFilePath, gui=True):
        Thread.__init__(self)

        self.lp = LP(self.rotateGui)
        self.leap = LeapController(self.notifyGui,self.calculateScale)

        self.scratchFilePath=scratchFilePath
        self.baseFilePath=baseFilePath

        self.gui = None


        if gui:

            stamp=time.time()+4

            def gui():

                self.gui=Visualisation(self.lp.radius)
                self.gui.run()


            t=Thread(target=gui)
            t.start()

            #self.loadStreams()

            time.sleep(stamp-time.time()+2)
            self.start()

        else:
            self.loadStreams()
            self.start()


    def loadStreams(self):
            self.scratchMusic = AudioController(self.scratchFilePath, scaleFunction=self.leap.getScale,
                                            volumeFunction=self.leap.getScratchCrossfade, stoppingFunction=self.stop)
            self.baseMusic = AudioController(self.baseFilePath, volumeFunction=self.leap.getBaseCrossfade,
                                             stoppingFunction=self.stop)


    def calculateScale(self,x1,y1,x2,y2):

        self.gui.pointing = True

        angle = self.lp.getAngle(x2, y2, x1, y1)

        ms=self.lp.degreesPerMillisecond
        t=(self.leap.timestamp-self.leap.prevTimestamp)

        normalDelta=t*ms


        if normalDelta==0:
            normalDelta=1

        scale=0 if angle == 0  else (angle /normalDelta)


        if abs(scale)<0.1:
            scale=0

        return scale


    def start(self):

        # self.scratchMusic.start()
        # self.baseMusic.start()
        self.lp.start()
        self.leap.start()

    def stop(self):
        self.lp.stopped = True

    def rotateGui(self, rot):
        if self.gui:
            self.gui.setRotation(rot)

    def notifyGui(self, breaking, scratching, scratchPosition=None, crossfade=(1, 0), volume=1, scale=1):
        if not self.gui:
            return
        self.gui.setCrossfader(crossfade[1])

        if scratching and scratchPosition:
            scratchPosition.x *= 3
            scratchPosition.z *=- 3

            self.gui.activateCursor(scratchPosition.x, scratchPosition.z)

            # # #TODO:
            if scratchPosition.x < self.lp.radius:
                scratchPosition.z *= -1

            self.lp.setPosition(scratchPosition.x/3.,scratchPosition.z/3.)


        elif breaking and scratchPosition:
            scratchPosition.x *= 3
            scratchPosition.z *= 3

            self.gui.activateCursor(scratchPosition.x, scratchPosition.z)
            self.lp.scratching = False
            self.lp.friction = scale
        else:
            self.lp.scratching = False
            self.gui.deactivateCursor()
            self.lp.friction = 1
        self.gui.setVolume(volume)


if __name__ == "__main__":
    c = Controller("output/beat.wav", "input/scratch.wav", gui=True)