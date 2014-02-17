import sys
sys.path.append("../common")

from threading import Thread
from AudioController import AudioController
from LeapController import LeapController
from Config import Config

class Controller(Thread):
    def __init__(self, baseFilePath,scratchFilePath):
        Thread.__init__(self)
        self.leap = LeapController()
        self.baseMusic = AudioController(baseFilePath, volumeFunction=self.leap.getBaseCrossfade)
        self.scratchMusik = AudioController(scratchFilePath, scaleFunction=self.leap.getScale, volumeFunction=self.leap.getScratchCrossfade)
        self.leap.start()

if __name__ == "__main__":

    base=Config.__getBaseFilePath__()
    scratch=Config.__getScratchFilePath__()

    Controller("../../input/"+base, "../../input/"+scratch)
