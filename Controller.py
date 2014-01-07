from threading import Thread
from AudioController import AudioController
from FileHandler import ScratchFileHandler,BaseFileHandler
from LeapController import LeapController


class Controller(Thread):
    def __init__(self, filePath):
        Thread.__init__(self)
        self.leap = LeapController()

        self.crossfade=(1,0)
        self.crossfadeRange=100

        self.scratchMusicSampler = AudioController(ScratchFileHandler(filePath), scaleFunction=self.leap.getScale, volumeFunction=self.getScratchCrossfade)

        self.baseMusicSampler=AudioController(BaseFileHandler(filePath),volumeFunction=self.getBaseCrossfade)

        self.start()
        self.baseMusicSampler.start()
        self.scratchMusicSampler.start()
        self.leap.start()



    def run(self):
        while True:
            pos=self.leap.getCrossfadePosition()

            if pos:
                div=pos/self.crossfadeRange

                if abs(div)<0.1:
                    self.crossfade =(0.5,0.5)
                self.crossfade=(0.5-div,0.5+div)

            print self.crossfade




    def getBaseCrossfade(self):
        return self.crossfade[0]

    def getScratchCrossfade(self):
        return self.crossfade[1]


if __name__ == "__main__":
    c = Controller("input/scratch.wav")
