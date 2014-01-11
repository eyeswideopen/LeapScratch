from threading import Thread

import os

class Visualisation():
    def __init__(self,radius):
        self.radius=radius
        self.dir=0
        self.pointing=False
        self.spriteCursor=None
        self.spriteCrossfader=None
        self.spriteSlider=None
        self.spriteVolume=None
        self.width=600
        self.height=480
        self.rotation=0


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

            scale=self.radius*2/float(picLp.width)
            spriteLp.scale=scale


            picSlider = pyglet.image.load('resources/slider.png')
            self.spriteSlider=pyglet.sprite.Sprite(picSlider)
            scale=width/float(self.spriteSlider.width)
            self.spriteSlider.scale=scale

            picCrossfader=pyglet.image.load('resources/pointer.png')
            picCrossfader.anchor_x = picCrossfader.width /2
            self.spriteCrossfader=pyglet.sprite.Sprite(picCrossfader)

            picVolume = pyglet.image.load('resources/volume.png')
            self.spriteVolume=pyglet.sprite.Sprite(picVolume)
            scale=50/float(self.spriteVolume.width)
            self.spriteVolume.scale=scale

            self.spriteVolume.x=0
            self.spriteVolume.y=height-50


            def close():
                os._exit(0)

            w.on_close=close

            def draw_rect(x, y, width, height,filled=True):
                param=pyglet.gl.GL_QUADS if filled else pyglet.gl.GL_LINE_LOOP
                pyglet.gl.glBegin(param)
                pyglet.gl.glVertex2f(x, y)
                pyglet.gl.glVertex2f(x, y + height)
                pyglet.gl.glVertex2f(x + width, y + height)                  # top right point
                pyglet.gl.glVertex2f(x + width, y)                           # bottom right point
                pyglet.gl.glEnd()




            def draw(e):
                w.clear()
                spriteLp.rotation=self.rotation
                spriteLp.draw()

                self.spriteVolume.draw()

                self.spriteSlider.draw()
                self.spriteCrossfader.draw()

                scale=400*self.volume/100
                pyglet.gl.glColor3f(255,255,255)
                draw_rect(70,height-40,410,30)
                pyglet.gl.glColor3f(0,0,0)
                draw_rect(75,height-35,400,20,False)
                pyglet.gl.glColor3f(255,0,0)
                draw_rect(75,height-35,scale,20)

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

    def setVolume(self,vol):
        self.volume=vol

    def setRotation(self,rot):
        self.rotation=rot

if __name__=="__main__":
    from LPSimulator import LP
    v=Visualisation(LP(0,0,50))
    v.start()
