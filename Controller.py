from Observer import Observer
from LeapAccsess import Access
from AudioPlayer import Sampler
from threading import Thread
from LPSimulator import LP
from Visualisation import Visualisation

class Controller(Observer,Thread):
    def __init__(self,filePath):
        Thread.__init__(self)
        Observer.__init__(self)

        radius=150
        self.lp=LP(0,0,radius)
        self.sampler=Sampler(filePath)
        self.leapAccess=Access()
        self.leapAccess.register(self)
        self.reverse=False
        self.scale=1
        self.start()
        self.visualisation=Visualisation(self.lp)
        self.visualisation.start()

        self.leapAccess.start()


    def run(self):
        while True:
            if self.scale>5 or self.scale<0.001:
                # if self.scale<0.001:
                #     print "to fast"
                # else:
                #     print("to low")
                continue
            self.sampler.playPart(self.reverse,self.scale)



    def notify(self):
        if not self.leapAccess.hand:
            self.lp.stopped=False
            self.scale=1
            self.reverse=False
            self.visualisation.pointing=False
            return

        path=self.leapAccess.getPath()

        if len(path)>1:

            self.lp.stopped=True

            self.visualisation.pointing=True
            self.visualisation.setCursor(path[-1]["x"],path[-1]["y"])

            angle=self.lp.getAngle(path[-1]["x"],path[-1]["y"],path[-2]["x"],path[-2]["y"])
            self.scale=1/(angle/self.lp.rotationDelta)

            if angle<0:
                self.reverse=True
            else:
                self.reverse=False

            self.scale=abs(self.scale)
            self.lp.addToRotation(angle)


if __name__=="__main__":
    c=Controller("output/file.wav")
