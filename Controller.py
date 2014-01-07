from threading import Thread
from AudioController import AudioController
from FileHandler import NewFileHandler
from LeapController import NewLeapController


class Controller(Thread):
    def __init__(self, filePath):
        Thread.__init__(self)
        self.leap = NewLeapController()
        self.sampler = AudioController(NewFileHandler(filePath), self.leap.getScale)
        self.start()
        self.sampler.start()
        self.leap.start()


if __name__ == "__main__":
    c = Controller("input/scratch.wav")
