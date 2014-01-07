from __future__ import division
from threading import Thread
from AudioController import BaseAudioController,ScratchAudioController
from FileHandler import FileHandler
from LPSimulator import LP
from LeapController import LeapController
from Visualisation import Visualisation


class Controller(Thread):
    def __init__(self, baseFilePath,scratchFilePath):
        Thread.__init__(self)
        self.leap = LeapController()

        self.crossfading=False
        self.crossfade=[0,1]
        self.crossfadeRange=100
        self.crossfadeBorders=(None, None)


        self.volume=100

        radius = 150
        self.lp = LP(0, 0, radius)


        self.scratchMusicSampler = ScratchAudioController(FileHandler(scratchFilePath), volumeFunction=self.getScratchCrossfade, scaleFunction=self.leap.getScale)

        self.baseMusicSampler=BaseAudioController(FileHandler(baseFilePath), volumeFunction=self.getBaseCrossfade)

        self.visualisation=Visualisation(self.lp)

        self.lp.start()
        #self.visualisation.start()
        self.start()


        self.baseMusicSampler.start()
        self.scratchMusicSampler.start()
        self.leap.start()


    def run(self):

        while True:
            div=self.leap.getCrossfade()

            if div:

                div/=75

                if abs(div)<0.01:
                    div=0

                self.crossfade[0]+=div
                self.crossfade[1]-=div

                if self.crossfade[0]>1: self.crossfade[0]=1
                if self.crossfade[0]<0: self.crossfade[0]=0
                if self.crossfade[1]>1: self.crossfade[1]=1
                if self.crossfade[1]<0: self.crossfade[1]=0


                self.visualisation.setCrossfader(self.crossfade[1])


            self.volume+=self.leap.getVolume()

            if self.volume>100:
                self.volume=100
            elif self.volume<0:
                self.volume=0

            print self.volume

    def getCrossfade(self):
        return self.crossfade

    def getBaseCrossfade(self):
        return self.crossfade[0]*(self.volume/100)

    def getScratchCrossfade(self):
        return self.crossfade[1]*(self.volume/100)


if __name__ == "__main__":
    c = Controller("output/beat.wav","input/scratch.wav")
