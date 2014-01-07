from threading import Thread

import os

class Visualisation():
    def __init__(self,lp):
        self.lp=lp
        self.dir=0
        self.pointing=False
        self.spriteCursor=None
        self.spriteCrossfader=None
        self.spriteSlider=None
        self.width=600
        self.height=480

        crossfadePosition=0.5


    def start(self):
        def init():
            import pyglet

            width=self.width
            height=self.height

            w=pyglet.window.Window(width,height)

            picHand = pyglet.image.load('resources/hand.png')
            picHand.anchor_y = picHand.height
            self.spriteCursor=pyglet.sprite.Sprite(picHand)

            picLp = pyglet.image.load('resources/platte.png')
            picLp.anchor_x = picLp.width /2
            picLp.anchor_y = picLp.height / 2

            spriteLp=pyglet.sprite.Sprite(picLp,width/2,height/2)

            scale=self.lp.radius*2/float(picLp.width)
            spriteLp.scale=scale


            picSlider = pyglet.image.load('resources/slider.png')
            self.spriteSlider=pyglet.sprite.Sprite(picSlider)
            scale=width/float(self.spriteSlider.width)
            print scale
            self.spriteSlider.scale=scale

            picCrossfader=pyglet.image.load('resources/pointer.png')
            picCrossfader.anchor_x = picCrossfader.width /2
            self.spriteCrossfader=pyglet.sprite.Sprite(picCrossfader)



            def close():
                os._exit(0)

            w.on_close=close


            def draw(e):
                w.clear()
                spriteLp.rotation=self.lp.rotation
                spriteLp.draw()

                self.spriteSlider.draw()
                self.spriteCrossfader.draw()



                if self.pointing:
                    self.spriteCursor.draw()

            pyglet.clock.schedule(draw)

            pyglet.app.run()


        t = Thread(target=init)
        t.start()

    def setCursor(self,x,y):
        if self.spriteCursor:
            self.spriteCursor.x=x+self.width/2
            self.spriteCursor.y=-y+self.height/2

    def setCrossfader(self,factor):
        if self.spriteCrossfader:

            self.spriteCrossfader.x=self.spriteSlider.width*factor

if __name__=="__main__":
    from LPSimulator import LP
    v=Visualisation(LP(0,0,50))
    v.start()
