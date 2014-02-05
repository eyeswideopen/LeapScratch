from __future__ import division
import math
from threading import Thread
import time


class LP(Thread):

    def __init__(self,updateFunction=lambda x: x,radius=200,x=None,y=None,):
        Thread.__init__(self)

        self.x=x or radius
        self.y=y or 0
        self.radius=radius
        self.revolution=45

        self.updateRotation=updateFunction

        self.rotation=0
        self.running=False
        self.scratching=False

        self.pos=None
        self.lastPos=None

        self.friction=1

        self.degreesPerMillisecond=(360*(self.revolution/60))/1000 #delta for every millisecond depending on revolutions per minute

        self.stopped=False
        self.timestamp=time.time()

    def addToRotation(self,angle):
        self.rotation+=angle

    def setPosition(self,x,y):
        self.lastPos=self.pos
        self.pos=(x,y)

        if self.pos and self.lastPos:
            self.scratching=True
            self.addToRotation(-self.getAngle(x,y,self.lastPos[0],self.lastPos[1]))

    def run(self):
        self.running=True

        while self.running:
            if self.stopped:
                continue

            if not self.scratching:
                self.rotation+=self.degreesPerMillisecond*self.friction

            self.updateRotation(self.rotation)
            time.sleep(0.001)

    def stop(self):
        self.running=False




    def getAngle(self,_x,_y,px,py):

        if _y-self.y==0 or py-self.y==0:
            return 0
        alpha1 =math.atan((_x-self.x) / (_y-self.y))
        alpha2 =math.atan((px-self.x) / (py-self.y))

        if alpha1>0:
            alpha1*=-1
        if alpha2>0:
            alpha2*=-1

        alpha = alpha2 - alpha1
        if _y>0:
            alpha*=-1

        return math.degrees(alpha)


    def getCircumferentialSpeed(self,d=None):
        dia=self.radius*2
        if d:
            dia=d

        speed=(dia*math.pi*self.revolution)/60*1000

        return speed

    def getDiameter(self):
        return self.radius*2

    def getCircumference(self):
        return self.radius*2*math.pi

    def getArea(self):
        return math.pow(self.radius,2)*math.pi

    def getDistance(self,x,y):
        dq=math.pow(self.x-x,2)+math.pow(self.y-y,2)
        return math.sqrt(dq)