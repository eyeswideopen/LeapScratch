from AudioController import AudioController
from FileHandler import FileHandler
from NewLeapController import NewLeapController
from threading import Thread

class Controller( Thread):
    def __init__(self, filePath):
        Thread.__init__(self)
        self.leap = NewLeapController()
        self.sampler = AudioController(FileHandler(filePath), self.leap.getScale)
        self.start()
        self.sampler.start()
        self.leap.start()

if __name__ == "__main__":
    c = Controller("output/file.wav")
