import sys, os, math
sys.path.append("lib")
import Leap
import collections


class NewLeapController(Leap.Listener):
    def __init__(self):
        Leap.Listener.__init__(self)
        self.path = collections.deque(maxlen=1000)
        self.lastFrame = None
        self.lastScale = 1.0

    def start(self):
        controller = Leap.Controller()
        controller.add_listener(self)
        sys.stdin.readline()

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
        self.path.append(controller.frame())

    def getScale(self):

        #pop next frame if available, else returns old scale
        frame = self.path.pop() if len(self.path) > 0 else None
        if not frame:
            return self.lastScale

        #gets the tracked position
        pos = self.getPos(frame)

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


        #return 0.5

        # frame = self.path.pop() if len(self.path) > 0 else None
        # if not frame:
        #     return self.lastScale
        #
        # if frame:
        #     pos = self.getPos(frame)
        #     translation, translationProb = self.getTranslation(frame)
        #
        #     ret = translation.x / 50 if pos and pos.y < 200 else self.lastScale
        #
        #     self.path.clear()
        #
        #     self.lastFrame = frame
        #
        #     if abs(abs(ret) - abs(self.lastScale))> 0.1:
        #         ret = self.lastScale + 0.1 if self.lastScale < ret else self.lastScale - 0.1
        #
        #     if abs(ret) < 0.005:
        #         ret = 0.0
        #
        #     ret = round(ret, 2)
        #
        #     self.lastScale = ret
        #
        #     return ret
        #
        #     # return 0.0 if abs(ret) < 0.3 else ret
        # return 1.0


if __name__ == "__main__":
    leap = NewLeapController()
    leap.start()