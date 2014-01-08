from threading import Thread
# from AudioController import AudioController
from fastAudioController import AudioController
from FileHandler import FileHandler
# from LeapController import LeapController
from fastLeapController import NewLeapController


class Controller(Thread):
    def __init__(self, leftFilePath, rightFilePath):
        Thread.__init__(self)
        self.leap = NewLeapController()

        self.leftSampler = AudioController(FileHandler(leftFilePath), self.leap.getScale)

        self.leap.start()


if __name__ == "__main__":
    c = Controller( "input/scratch.wav","input/scratch.wav")
