from Observer import Observer
from LeapAccsess import Access
from AudioPlayerCB import Sampler
from threading import Thread
from LPSimulator import LP
from Visualisation import Visualisation

import collections

import sci

import time


class Controller(Observer, Thread):
    def __init__(self, filePath):
        Thread.__init__(self)
        Observer.__init__(self)

        radius = 150
        self.lp = LP(0, 0, radius)
        self.sampler = Sampler(filePath,self.getVectorList)
        self.leapAccess = Access()
        self.reverse = False
        self.scale = 1
        self.visualisation = Visualisation(self.lp)

        self.prevCoordinate=None
        self.timestamp=None
        self.prevTimestamp=None

        self.start()
        #self.visualisation.start()

        self.leapAccess.start()




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

        scale=0 if angle == 0  else 1/ (angle /normalDelta)


        #self.scale = abs(self.scale)
        self.lp.addToRotation(angle)

        if scale>1:
            pass
            #print(x1,y1,x2,y2)

        if abs(scale)>1000.0 or abs(scale)<0.0001:
            scale=0


        return scale

    def getVectorList(self):

        path=self.leapAccess.path

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
        elif not self.leapAccess.tracking:
            self.lp.stopped = False
            self.visualisation.pointing = False
            return 1
        return 0




        # data=collections.deque(maxlen=numberOfVectors)
        #
        # if not self.prevTimestamp:
        #     self.prevTimestamp=int(round(time.time() * 1000))
        #
        # if len(path)<1:
        #     return data
        #
        #
        #
        # increments=0
        # if len(path)/numberOfVectors<1:
        #     increments=1
        # else:
        #     increments=len(path)/numberOfVectors
        #
        #
        # print(len(path))
        #
        # for i in range(0,len(path),increments):
        #
        #     if len(data)>=numberOfVectors:
        #         break
        #
        #     nextPos=i+increments-1
        #
        #     if len(data)==numberOfVectors-1:
        #         nextPos=len(path)-1
        #
        #
        #     self.timestamp=int(round(time.time() * 1000))
        #     scale=self.calculateScale(path[i]["x"],path[i]["y"],path[nextPos]["x"],path[nextPos]["y"])
        #     self.prevTimestamp=self.timestamp
        #
        #     data.append(scale)
        #
        #
        # path.clear()


        # #TODO: Berechnung der Laenge der Ausgabe in Controller; Path irgendwie richtig leeren/Index ...
        #
        # return data


    def run(self):

        while True:
            pass
            # v=self.getVectorList(3)
            # if v:
            #     print(v)
            # import time
            # time.sleep(1)
            # #self.sampler.playPart(self.reverse)


    def notify(self):

        if not self.leapAccess.tracking:
            self.lp.stopped = False
            self.scale = 1
            self.reverse = False
            self.visualisation.pointing = False
            return

        path = self.leapAccess.getPath()

        if len(path) > 1:

            self.lp.stopped = True

            self.visualisation.pointing = True
            self.visualisation.setCursor(path[-1]["x"], path[-1]["y"])

            angle = self.lp.getAngle(path[-1]["x"], path[-1]["y"], path[-2]["x"], path[-2]["y"])
            self.scale = 1 / (angle / self.lp.degreesPerMillisecond)

            if angle < 0:
                self.reverse = True
            else:
                self.reverse = False

            self.scale = abs(self.scale)
            self.lp.addToRotation(angle)


if __name__ == "__main__":
    c = Controller("output/file2.wav")
