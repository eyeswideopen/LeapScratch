from threading import Thread
import time
import AudioController

from LeapController import LeapController
from LPSimulator import LP
from OLD import FileHandler
from Visualisation import Visualisation


class Controller( Thread):
    def __init__(self, filePath):
        Thread.__init__(self)


        self.leap = LeapController()



        radius = 150
        self.lp = LP(0, 0, radius)
        self.sampler = AudioController(FileHandler(filePath),self.getScale)

        self.visualisation = Visualisation(self.lp)

        self.prevCoordinate=None
        self.timestamp=None
        self.prevTimestamp=None

        self.start()
        self.lp.start()
        self.sampler.start()
        self.visualisation.start()
        self.leap.start()


    def calculateScale(self,x1,y1,x2,y2):

        #auslagern in leap callback
        self.lp.stopped = True
        self.visualisation.pointing = True

        self.visualisation.setCursor(x2,y2)
        angle = self.lp.getAngle(x2, y2, x1, y1)

        ms=self.lp.degreesPerMillisecond
        t=(self.timestamp-self.prevTimestamp)

        normalDelta=t*ms


        if normalDelta==0:
            normalDelta=1

        scale=0 if angle == 0  else (angle /normalDelta)

        self.lp.addToRotation(angle)

        if abs(scale)<0.1:
            scale=0

        return scale

    def getScale(self):

        path=self.leap.path

        if not self.prevCoordinate and len(path)>=2:
            self.prevCoordinate=path.popleft()
            self.prevTimestamp=int(round(time.time() * 1000))
        elif not self.prevCoordinate:
            return 1

        if len(path)>=1:
            coordinate=path.pop()
            self.timestamp=int(round(time.time() * 1000))
            path.clear()
            scale= self.calculateScale(self.prevCoordinate["x"],self.prevCoordinate["y"],coordinate["x"],coordinate["y"])
            self.prevCoordinate=coordinate
            self.prevTimestamp=self.timestamp

            return scale
        elif not self.leap.tracking:
            self.lp.stopped = False
            self.visualisation.pointing = False
            return 1
        return 0


if __name__ == "__main__":
    c = Controller("output/file.wav")
