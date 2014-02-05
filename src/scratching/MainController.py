import sys
sys.path.append("../common")

from threading import Thread
from AudioController import AudioController
from LeapController import LeapController

class fastController(Thread):
    def __init__(self, filePath):
        Thread.__init__(self)
        self.leap = LeapController()
        self.leftSampler = AudioController(filePath, self.leap.getScale, self.leap.getMasterVolume)
        self.leap.start()

if __name__ == "__main__":
    c = fastController( "../../input/scratch.wav")
