from threading import Thread
from LPSimulator import LP
from Visualisation import Visualisation
from fastLeapController import LeapController
from fastAudioController import AudioController
from FileHandler import FileHandler

from samysFastAudioController import AudioController
from samysFileHandler import FileHandler

class Controller(Thread):
    def __init__(self, baseFilePath, scratchFilePath):
        Thread.__init__(self)
        self.leap = LeapController(self.notifyGui)

        self.lp=LP(self.rotateGui)
        self.gui=Visualisation(self.lp.radius)

        self.lp.start()

        AudioController(FileHandler(scratchFilePath),scaleFunction=self.leap.getScale,volumeFunction=self.leap.getScratchCrossfade)
        AudioController(FileHandler(baseFilePath),volumeFunction=self.leap.getBaseCrossfade)

        #self.gui.start()
        self.leap.start()

    def rotateGui(self,rot):
        self.gui.setRotation(rot)

    def notifyGui(self,scratching,scratchPosition=None,crossfade=(1,0),volume=1):
        self.gui.setCrossfader(crossfade[1])
        if scratching and scratchPosition:
            self.gui.pointing=True
            self.gui.setCursor(scratchPosition.x,scratchPosition.z)
            self.lp.setPosition(scratchPosition)
        else:
            self.gui.pointing=False
            self.lp.scratching=False
        self.gui.setVolume(volume)




if __name__ == "__main__":
    c = Controller( "output/beat.wav","output/vocal.wav")