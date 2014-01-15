from threading import Thread
from fastAudioController import AudioController
from fastLeapController import fastLeapController

class fastController(Thread):
    def __init__(self, filePath):
        Thread.__init__(self)
        self.leap = fastLeapController()
        self.leftSampler = AudioController(filePath, self.leap.getScale, self.leap.getMasterVolume)
        self.leap.start()

if __name__ == "__main__":
    c = fastController( "input/scratch.wav")
