import sys
sys.path.append("../../src/common")
from threading import Thread
from LPSimulator import LP
from Visualisation import Visualisation
from LeapController import LeapController
from AudioController import AudioController
from Config import Config


class Controller(Thread):
    def __init__(self, baseFilePath, scratchFilePath, gui=True):
        Thread.__init__(self)

        self.lp=LP(self.rotateGui)
        self.leap = LeapController(self.notifyGui)

        self.gui = None

        if gui:
            self.gui = Visualisation(self.lp.radius)
            self.gui.start()


        self.scratchMusic = AudioController(scratchFilePath, scaleFunction=self.leap.getScale,
                                            volumeFunction=self.leap.getScratchCrossfade, stoppingFunction=self.stop)
        self.baseMusic = AudioController(baseFilePath, volumeFunction=self.leap.getBaseCrossfade,
                                         stoppingFunction=self.stop)

        self.start()


    def start(self):

        self.scratchMusic.start()
        self.baseMusic.start()
        self.lp.start()
        self.leap.start()


    def stop(self):
        self.lp.stopped=True


    def rotateGui(self, rot):
        self.gui.setRotation(rot)

    def notifyGui(self, breaking, scratching, scratchPosition=None, crossfade=(0, 1), volume=1, scale=1):
        if not self.gui:
            return
        self.gui.setCrossfader(crossfade[1])

        if scratching and scratchPosition:
            self.gui.pointing = True
            scratchPosition.x *= 3
            scratchPosition.z *= -3

            self.gui.setCursor(scratchPosition.x, scratchPosition.z)

            if scratchPosition.x > self.lp.radius: scratchPosition.z *= -1

            self.lp.setPosition(scratchPosition.x,scratchPosition.z)

        elif breaking:
            self.gui.pointing = True
            self.lp.scratching = False
            self.lp.friction = scale
        else:
            self.lp.scratching = False
            self.gui.pointing = False
            self.lp.friction = 1
        self.gui.setVolume(volume)


if __name__ == "__main__":

    base=Config.__getBaseFilePath__()
    scratch=Config.__getScratchFilePath__()

    Controller("../../input/"+base, "../../input/"+scratch,gui=True)