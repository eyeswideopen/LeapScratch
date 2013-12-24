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
        #return 0.5
        frame = self.path.pop() if len(self.path) > 0 else None
        if frame:
            pos = self.getPos(frame)
            translation, translationProb = self.getTranslation(frame)
            ret = translation.x / 15 if pos and pos.y < 200 else 1.0
            self.path.clear()
            self.lastFrame = frame

            if abs(ret) - abs(self.lastScale)> 0.1:
                ret = ret - 0.1 if self.lastScale < ret else ret + 0.001
            self.lastScale = ret
            #TODO: wasn das
            return ret
            print 0.0 if abs(ret) < 0.1 else ret
            return 0.0 if abs(ret) < 0.3 else ret
        return 1.0


if __name__ == "__main__":
    leap = NewLeapController()
    leap.start()