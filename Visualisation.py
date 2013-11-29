import pygame,sys

from threading import Thread


class LongplayerSprite(pygame.sprite.Sprite):

    def __init__(self,x,y,radius):
        pygame.sprite.Sprite.__init__(self)
        self.imageMaster = pygame.image.load("resources/platte.png")
        self.imageMaster = self.imageMaster.convert()


        self.diameter=radius*2

        self.dir = 0

        self.imageMaster=pygame.transform.scale(self.imageMaster,(self.diameter,self.diameter))
        self.image = self.imageMaster
        self.rect = self.image.get_rect()

        self.rect.center = (radius, radius)

        self.x=x
        self.y=y
        self.rect.x=self.x
        self.rect.y=self.y



    def update(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, int(self.dir))

        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        self.rect.center = oldCenter




class Visualisation(Thread):

    def __init__(self,lp):
        Thread.__init__(self)
        # Initialize the game engine

        self.lp=lp
        self.width=600
        self.height=480

        self.point=[0,0,5,5]

        self.pointing=False

        self.sprite=None

    def setPoint(self,x,y):
        self.point[0]=x+self.width/2
        self.point[1]=y+self.height/2


    def run(self):
        pygame.init()

        screen=pygame.display.set_mode((self.width,self.height))

        self.clock = pygame.time.Clock()
        self.sprite=LongplayerSprite(self.width/2-self.lp.radius,self.height/2-self.lp.radius,self.lp.radius)

        allSprites = pygame.sprite.Group(self.sprite)


        while True:
            if self.sprite:
                self.sprite.dir=self.lp.rotation

            allSprites.update()

            screen.fill((0,0,0))


            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.
            self.clock.tick(10)

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    sys.exit(0)


            if self.pointing:
                pygame.draw.ellipse(screen,(0,0,255),self.point)


            allSprites.draw(screen)

            if self.pointing:
                pygame.draw.ellipse(screen,(0,0,255),self.point)

            pygame.display.flip()




        # Be IDLE friendly
        pygame.quit ()


if __name__=="__main__":
    v=Visualisation()
    v.start()