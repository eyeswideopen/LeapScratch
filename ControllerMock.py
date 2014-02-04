from threading import Thread
import time,pickle
from Visualisation import Visualisation
from LPSimulator import LP


class Controller(Thread):
    def __init__(self):
        super(self.__class__,self).__init__()

        self.positions = pickle.load( open( "positions.p", "rb" ) )
        self.volumes = pickle.load( open( "volumes.p", "rb" ) )
        self.crossfades = pickle.load( open( "crossfades.p", "rb" ) )


        self.lp=LP(updateFunction=self.rotateGui)
        self.gui=Visualisation(self.lp.radius)

        self.gui.start()
        self.lp.start()

    def rotateGui(self, rot):
        self.gui.setRotation(rot)

    def run(self):

        i=0
        while True:
            time.sleep(0.01)
            p=self.positions[i]
            c=self.crossfades[i]
            v=self.volumes[i]

            if p!=None:
                self.gui.setCursor(p[0],p[1])
                self.lp.scratching=True
            else:
                self.lp.scratching=False
                self.gui.pointing=False

            if c!=None:
                self.gui.setCrossfader(c)

            if v!=None:
                self.gui.setVolume(v)

            i+=1



if __name__=="__main__":
    c=Controller()
    c.start()