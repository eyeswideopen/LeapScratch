from Observer import Observer
from LeapAccsess import Access
from audio_long import Sampler
from threading import Thread

from LPSimulator import LP

class Controller(Observer,Thread):
    def __init__(self,filePath):
        Thread.__init__(self)
        Observer.__init__(self)

        self.lp=LP(0,0,50)
        self.sampler=Sampler(filePath)

        self.leapAccess=Access()
        self.leapAccess.register(self)

        self.reverse=False
        self.scale=1

        self.start()
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
            self.scale=1
            self.reverse=False
            return

        data=self.leapAccess.getPath()

        # s=data[0]
        # d=self.lp.getDistance(s["x"],s["y"])
        #
        # normalSpeed=self.lp.getCircumferentialSpeed()
        #
        # speed=self.lp.getCircumferentialSpeed(d)
        #scale=speed/normalSpeed


        if len(data)>1:
            angle=self.lp.getAngle(data[-1]["x"],data[-1]["y"],data[-2]["x"],data[-2]["y"])
            self.scale=1/(angle/self.lp.rotationDelta)


            if angle<0:
                self.reverse=True
            else:
                self.reverse=False

            self.scale=abs(self.scale)

            #print(self.scale)




if __name__=="__main__":
    c=Controller("output/file.wav")

