import sys, os, math

sys.path.append("lib")

import Leap

import collections


class LeapController(Leap.Listener):
    def __init__(self):
        Leap.Listener.__init__(self)
        self.path = collections.deque(maxlen=1000)

        self.tracking = False

        self.lastDistx = None
        self.lastDisty = None
        self.lastPointingPos = None
        self.point = None

        self.lastCallbackPos = None

    def start(self):
        controller = Leap.Controller()
        controller.add_listener(self)
        sys.stdin.readline()

    def stop(self):
        os._exit(0)

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        # controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        # controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        # controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        # controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def bottommost(self, pointables):
        if pointables.is_empty:
            return None

        depth = {p.tip_position.y: p for p in pointables}

        y = min(depth.keys())
        deepest = depth[y]
        return deepest


    def on_frame(self, controller):

        frame = controller.frame()

        if not frame.hands.is_empty:

            hand = frame.hands.rightmost
            handPos = hand.palm_position

            currentPoint = self.bottommost(hand.fingers)

            pos = None

            if currentPoint:

                if not self.point or self.point.id == currentPoint.id:
                    pos = currentPoint.tip_position
                    self.point = currentPoint

                    self.lastDistx = math.sqrt(math.pow(pos.x - handPos.x, 2))
                    self.lastDisty = math.sqrt(math.pow(pos.z - handPos.z, 2))
                    self.lastPointingPos = pos

            if not pos:
                #print("before:",self.lastDistx,self.lastDisty,self.lastPointingPos.x,self.lastPointingPos.z,handPos.x,handPos.z)

                if self.lastDistx and self.lastDisty:
                    if handPos.x < self.lastPointingPos.x:
                        handPos.x -= self.lastDistx
                    else:
                        handPos.x -= self.lastDistx

                    if handPos.z < self.lastPointingPos.z:
                        handPos.z += self.lastDisty
                    else:
                        handPos.z -= self.lastDisty

                pos = handPos

                # print("after:",self.lastPointingPos.x,self.lastPointingPos.z,handPos.x,handPos.z)
                # print '\n'

            if pos:
                if pos.y < 200:
                    self.path.append({"x": pos.x, "y": pos.z})
                    self.tracking = True

                else:
                    self.path.clear()
                    self.tracking = False

        else:
            self.tracking = False
            self.path.clear()
            self.point = None


    def getScale(self):

        normalDistance = 20
        if not len(self.path) == 0:
            #TODO: failsafe bei init mit tracking. knallt vermutlich

            x=self.path.pop()["x"]

            if not self.lastCallbackPos:
                self.lastCallbackPos = x

            scale=x/ normalDistance

            self.lastCallbackPos=x

            return scale

        return 1.0
