from __future__ import division
import math

from threading import Thread

import time


class LP(Thread):

    def __init__(self,x,y,radius):
        Thread.__init__(self)

        self.x=x
        self.y=y
        self.radius=radius
        self.revolution=45

        self.rotation=0
        self.running=True

        self.rotationDelta=(360*(self.revolution/60))/100 #delta for every millisecond depending on revolutions per minute

        self.stopped=False
        self.t=time.time()
        self.start()

    def addToRotation(self,angle):
        self.rotation+=angle

    def run(self):

        while self.running:
            if self.stopped:
                continue
            if self.rotation>=360:
                self.rotation=0
            self.rotation+=self.rotationDelta
            time.sleep(0.01)

    def stop(self):
        self.running=False

    def getAngle(self,_x,_y,px,py):
        alpha1 =math.atan((_x-self.x) / (_y-self.y))
        alpha2 =math.atan((px-self.x) / (py-self.y))
        alpha = alpha2 - alpha1

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