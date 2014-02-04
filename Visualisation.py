from threading import Thread

import os,time


class Visualisation():
    def __init__(self, radius):
        self.radius = radius
        self.dir = 0
        self.pointing = False
        self.spriteCursor = None
        self.spriteSliderCrossfade = None
        self.spriteSliderVolume = None
        self.width = 1024
        self.height = 640
        self.rotation = 0
        self.crossfadeRange = (-90, 90)
        self.volumeRange = (-120, 120)


    def start(self):
        def init():
            import pyglet

            width = self.width
            height = self.height

            w = pyglet.window.Window(width, height,visible=False)


            picBackground = pyglet.image.load('resources/background.png')
            spriteBackground = pyglet.sprite.Sprite(picBackground)
            scale = width / float(spriteBackground.width)
            spriteBackground.scale = scale

            picForeground = pyglet.image.load('resources/topLayer.png')
            spriteForeground = pyglet.sprite.Sprite(picForeground)
            scale = width / float(spriteForeground.width)
            spriteForeground.scale = scale

            picHand = pyglet.image.load('resources/hand.png')
            picHand.anchor_y = picHand.height
            self.spriteCursor = pyglet.sprite.Sprite(picHand)

            picLp = pyglet.image.load('resources/platte.png')
            picLp.anchor_x = picLp.width / 2
            picLp.anchor_y = picLp.height / 2

            spriteLp = pyglet.sprite.Sprite(picLp, width / 2 + 32, height / 2)

            scale = 0.355
            spriteLp.scale = scale

            picSliderCrossfade = pyglet.image.load('resources/slider_crossfade.png')
            self.spriteSliderCrossfade = pyglet.sprite.Sprite(picSliderCrossfade)
            scale = width / float(self.spriteSliderCrossfade.width)
            self.spriteSliderCrossfade.scale = scale

            picSliderVolume = pyglet.image.load('resources/slider_masterVolume.png')
            self.spriteSliderVolume = pyglet.sprite.Sprite(picSliderVolume)
            scale = width / float(self.spriteSliderVolume.width)
            self.spriteSliderVolume.scale = scale



            def close():
                os._exit(0)

            w.on_close = close

            def draw(e):
                self.timestamp=t
                w.clear()

                spriteBackground.draw()

                spriteLp.rotation = self.rotation
                spriteLp.draw()

                self.spriteSliderCrossfade.draw()
                self.spriteSliderVolume.draw()

                spriteForeground.draw()

                if self.pointing:
                    self.spriteCursor.draw()



            pyglet.clock.schedule(draw)

            w.set_visible(True)

            pyglet.app.run()


        t = Thread(target=init)
        t.start()



    def setCursor(self, x, y):
        if self.spriteCursor:
            self.pointing=True
            self.spriteCursor.x = int(round(x + self.width / 2)) - self.radius
            self.spriteCursor.y = int(round(y + self.height / 2))

    def setCrossfader(self, factor):
        if self.spriteSliderCrossfade:
            dis = abs(self.crossfadeRange[1] - self.crossfadeRange[0])
            self.spriteSliderCrossfade.x = self.crossfadeRange[0] + dis * factor

    def setVolume(self, vol):
        if self.spriteSliderVolume:
            dis = abs(self.volumeRange[1] - self.volumeRange[0])
            self.spriteSliderVolume.y = self.volumeRange[0] + dis * (vol / 100.)

    def setRotation(self, rot):
        self.rotation = rot


if __name__ == "__main__":
    from LPSimulator import LP

    v = Visualisation(LP(0, 0, 50))
    v.start()
