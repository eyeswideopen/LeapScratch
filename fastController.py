from threading import Thread
from fastAudioController import AudioController
from fastLeapController import LeapController

class fastController(Thread):
    def __init__(self, filePath,enes):
        Thread.__init__(self)
        self.leap = LeapController(lambda x,y,s,f,d,t:x )
        self.leftSampler = AudioController(filePath, self.leap.getScale)
        self.leap.start()

if __name__ == "__main__":
    c = fastController( "input/scratch.wav","input/scratch.wav")
