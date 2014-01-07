import sys, os, math
sys.path.append("lib")
import Leap
import collections


class LeapController(Leap.Listener):
    def __init__(self):
        Leap.Listener.__init__(self)
        self.path = collections.deque(maxlen=1000)
        self.lastFrame = None
        self.frame=None
        self.lastScale = 1.0

        self.lastCrossfadePos=None

        self.gestured=False


    def start(self):
        controller = Leap.Controller()
        controller.add_listener(self)
        sys.stdin.readline()

    def stop(self):
        os._exit(0)

    def getScratchPos(self, frame):
        if frame.hands.is_empty:
            return None
        if len(frame.hands.rightmost.fingers) > 0:
            return min(frame.hands.rightmost.fingers, key=lambda finger: finger.tip_position.y).tip_position
        return frame.hands.rightmost.palm_position


    def getTranslation(self, frame):
        if self.lastFrame:
            return frame.translation(self.lastFrame), frame.translation_probability(self.lastFrame)
        return None, None


    def on_connect(self, controller):
        print "Connected"

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)


    def on_frame(self, controller):

        frame=controller.frame()
        gestures=frame.gestures()
        self.frame=frame

        if len(gestures):
            if gestures[0].type==Leap.Gesture.TYPE_CIRCLE:
                self.gestured=True
                return

        self.gestured=False

        self.path.append(frame)



    def getVolume(self):
        if not self.gestured:
            return 0

        gesture=self.frame.gestures()[0]
        circle=Leap.CircleGesture(gesture)

        if circle.pointables[0].direction.angle_to(circle.normal) <= math.pi/2:
            return 0.01

        else:
            return -0.01


    def getCrossfade(self):


        if not self.frame or self.gestured:
            self.lastCrossfadePos=None
            return

        hands=self.frame.hands

        if len(hands)>1:
            hand=hands.leftmost

            if hand.palm_position.y<200:
                if not self.lastCrossfadePos:
                    self.lastCrossfadePos=hand.palm_position.x
                    return

                x=self.lastCrossfadePos
                y=hand.palm_position.x

                dis=abs(x-y)

                if x>y:
                    self.lastCrossfadePos=y
                    return dis
                self.lastCrossfadePos=y
                return -dis

        self.lastCrossfadePos=None

        

    def getScale(self):

        #pop next frame if available, else returns old scale
        frame = self.path.pop() if len(self.path) > 0 else None
        if not frame or self.gestured:
            return self.lastScale

        #gets the tracked position
        pos = self.getScratchPos(frame)

        #estimates if translation is present since last frame
        translation, translationProb = self.getTranslation(frame)
        self.lastFrame = frame

        scale = translation.x / 3 if pos and pos.y < 200 else 1.0

        #clears path of used frames
        self.path.clear()

        #
        threshold = 0.2
        if abs(abs(scale) - abs(self.lastScale))> threshold:
            scale = self.lastScale + threshold if self.lastScale < scale else self.lastScale - threshold

        if abs(scale) < 0.2:
            scale = 0.0

        scale = round(scale, 2)

        self.lastScale = scale

        return scale


if __name__ == "__main__":
    leap = LeapController()
    leap.start()