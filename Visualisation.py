from threading import Thread

import os

class Visualisation():
    def __init__(self,lp):
        self.lp=lp
        self.dir=0
        self.pointing=False
        self.cursor=None
        self.width=600
        self.height=480


    def start(self):
        def event_loop():
            import pyglet

            width=self.width
            height=self.height

            w=pyglet.window.Window(width,height)

            pic = pyglet.image.load('resources/hand.png')
            pic.anchor_y = pic.height
            self.cursor=pyglet.sprite.Sprite(pic)

            pic = pyglet.image.load('resources/platte.png')
            pic.anchor_x = pic.width /2
            pic.anchor_y = pic.height / 2

            sprite=pyglet.sprite.Sprite(pic,width/2,height/2)

            scale=self.lp.radius*2/pic.width
            sprite.scale=scale

            def close():
                os._exit(0)

            w.on_close=close

            def draw(e):
                w.clear()
                sprite.rotation=self.lp.rotation
                sprite.draw()


                if self.pointing:
                    self.cursor.draw()

            #pyglet.clock.set_fps_limit(60)
            pyglet.clock.schedule(draw)

            pyglet.app.run()


        t = Thread(target=event_loop)
        t.start()

    def setCursor(self,x,y):
        if self.cursor:
            self.cursor.x=x+self.width/2
            self.cursor.y=-y+self.height/2

if __name__=="__main__":
    from LPSimulator import LP
    v=Visualisation(LP(0,0,50))
    v.start()
