import sys, os, math,platform

sys.path.append("../../lib")

p=platform.architecture()


if p[1].startswith('Win'):
    arch="win64"
    if p[0]=="32bit":
        arch="win32"
    sys.path.append("../../lib/"+arch)

elif p[1].startswith('ELF'):
    arch="x64"
    if p[0]=="32bit":
        arch="x86"
    sys.path.append("../../lib/"+arch)

else:
    sys.path.append("../../lib/mac")
	



import Leap
import collections


class LeapController(Leap.Listener):
    def __init__(self):
        Leap.Listener.__init__(self)
        self.path = collections.deque(maxlen=1000)
        self.lastFrame = None
        self.lastScale = 1.0
        self.volume = 100




    def on_connect(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)


    def start(self):
        controller = Leap.Controller()
        controller.add_listener(self)
        sys.stdin.readline()


    def getMasterVolume(self):
        return self.volume / 100.

    def stop(self):
        os._exit(0)

    def getPos(self, frame):
        if frame.hands.is_empty:
            return None
        if len(frame.hands.rightmost.fingers) > 0:
            return min(frame.hands.rightmost.fingers, key=lambda finger: finger.tip_position.y).tip_position
        return frame.hands.rightmost.palm_position

    def getTranslation(self, frame):
        if self.lastFrame:
            return frame.translation(self.lastFrame), frame.translation_probability(self.lastFrame)
        return None, None

    def on_frame(self, controller):

        frame = controller.frame()
        gestures = frame.gestures()
        self.frame = frame

        if len(gestures) > 0:
            if gestures[0].type == Leap.Gesture.TYPE_CIRCLE:
                circle = Leap.CircleGesture(gestures[0])
                if circle.center[1] > 250:
                    self.volume += 1 if circle.pointables[0].direction.angle_to(circle.normal) <= math.pi / 2 else -1

                    if self.volume > 100:
                        self.volume = 100
                    elif self.volume < 0:
                        self.volume = 0



        self.gestured = False
        self.path.append(frame)

    def getScale(self):
        #pop next frame if available, else returns old scale
        frame = self.path.pop() if len(self.path) > 0 else None
        if not frame:
            return self.lastScale

        pos = self.getPos(frame)
        translation, translationProb = self.getTranslation(frame)
        self.lastFrame = frame

        #slowdoooooown
        if pos and pos.y < 150:
            scale = translation.x / 4
        elif pos and pos.y < 250:
            scale = (pos.y - 150) / 100

        else:
            scale = 1

        self.path.clear()

        threshold = 0.3
        if abs(abs(scale) - abs(self.lastScale)) > threshold:
            scale = self.lastScale + threshold if self.lastScale < scale else self.lastScale - threshold

        if abs(scale) < 0.1:
            scale = 0.0

        scale = round(scale, 2)

        self.lastScale = scale
        return scale
