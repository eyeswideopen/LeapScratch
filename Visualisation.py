import pyglet

class Visualisation(pyglet.window.Window):

    def __init__(self,lp):
        self.w=int(600)
        self.h=int(480)
        pyglet.window.Window.__init__(self,self.w,self.h)
        self.lp=lp
        self.pointing=False

        pic = pyglet.image.load('resources/platte.png')
        pic.anchor_x = pic.width /2
        pic.anchor_y = pic.height / 2

        self.sprite=pyglet.sprite.Sprite(pic,self.w/2,self.h/2)

        scale=lp.radius*2/pic.width
        self.sprite.scale=scale
        self.dir=0

        pic = pyglet.image.load('resources/hand.png')
        pic.anchor_y = pic.height
        self.cursor=pyglet.sprite.Sprite(pic)

        pyglet.clock.set_fps_limit(60)
        self.drawingFunc=lambda x:x
        pyglet.clock.schedule(self.drawingFunc)

        self.pointing=False


    # def on_mouse_press(self,x, y, button, modifiers):
    #     self.pointing=True
    #     self.setCursor(x,y)
    #
    # def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
    #     self.pointing=True
    #     self.setCursor(x,y)
    #
    #
    # def on_mouse_release(self,x, y, button, modifiers):
    #     self.pointing=False

    def setCursor(self,x,y):
        self.cursor.x=x
        self.cursor.y=y

    def start(self):
        pyglet.app.run()


    def on_draw(self):
        self.clear()
        self.sprite.rotation=self.lp.rotation
        self.sprite.draw()
        if self.pointing:
            self.cursor.draw()


if __name__=="__main__":
    from LPSimulator import LP
    v=Visualisation(LP(0,0,50))
    v.start()
