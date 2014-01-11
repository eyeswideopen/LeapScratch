from threading import Thread
from LPSimulator import LP
from Visualisation import Visualisation
from LeapController import LeapController
from AudioController import AudioController


class Controller(Thread):
    def __init__(self, baseFilePath, scratchFilePath,gui=True):
        Thread.__init__(self)

        self.lp=LP(self.rotateGui)
        self.leap = LeapController(self.notifyGui)

        self.gui=None

        if gui:
            self.gui=Visualisation(self.lp.radius)
            self.gui.start()

        self.lp.start()

        AudioController(scratchFilePath,scaleFunction=self.leap.getScale,volumeFunction=self.leap.getScratchCrossfade)
        AudioController(baseFilePath,volumeFunction=self.leap.getBaseCrossfade)
        self.leap.start()

    def rotateGui(self,rot):
        self.gui.setRotation(rot)

    def notifyGui(self,breaking,scratching,scratchPosition=None,crossfade=(1,0),volume=1,scale=1):
        if not self.gui:
            return
        self.gui.setCrossfader(crossfade[1])

        if scratching and scratchPosition:
            self.gui.pointing=True
            scratchPosition.x*=2
            scratchPosition.z*=-2

            self.gui.setCursor(scratchPosition.x,scratchPosition.z)

            scratchPosition.z*=-1
            self.lp.setPosition(scratchPosition)
        elif breaking:
            self.gui.pointing=True
            self.lp.scratching=False
            self.lp.friction=scale
        else:
            self.lp.scratching=False
            self.gui.pointing=False
            self.lp.friction=1
        self.gui.setVolume(volume)




if __name__ == "__main__":
    c = Controller( "output/beat.wav","input/scratch.wav",gui=True)