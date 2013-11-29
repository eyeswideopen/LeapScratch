import sys
sys.path.append("lib")

import Leap
from Observable import Observable


class Access(Leap.Listener,Observable):

    def __init__(self):
        Leap.Listener.__init__(self)
        Observable.__init__(self)
        self.path=[]
        self.hand=False

    def start(self):
        controller = Leap.Controller()
        controller.add_listener(self)
        sys.stdin.readlines()

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def getPath(self):
        return self.path

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        if not frame.hands.is_empty:
            hand = frame.hands.rightmost

            # Check if the hand has any fingers
            fingers = hand.fingers
            if not fingers.is_empty:
                self.hand=True
                # Calculate the hand's average finger tip position
                depth =[finger.tip_position.y for finger in fingers]

                f=fingers.leftmost

                lowest=min(depth)
                if lowest<200:
                    self.path.append({"x":f.tip_position.x,"y":f.tip_position.z})

                elif len(self.path)>0:
                    self.path=[]
                    self.hand=False
                else:
                    self.hand=False

            elif len(self.path)>0:
                self.hand=False
                self.path=[]

        elif len(self.path)>0:
            self.hand=False
            self.path=[]

        self.notifyObservers()


if __name__=="__main__":
    a=Access()
    a.start()