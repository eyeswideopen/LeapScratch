from threading import Thread
from AudioController import AudioController
from FileHandler import FileHandler
from LeapController import LeapController


class Controller(Thread):
    def __init__(self, leftFilePath, rightFilePath):
        Thread.__init__(self)
        self.leap = LeapController()
        self.leftSampler = AudioController(FileHandler(leftFilePath),
                                           FileHandler(rightFilePath),
                                           volumeFunction=self.leap.getCrossfade, scaleFunction=self.leap.getScale)

        # self.rightSampler = AudioController(NewFileHandler(rightFilePath),
        #                                    scaleFunction=self.leap.getScale,
        #                                    volumeFunction=self.leap.getRightCrossfade)

        self.start()
        self.leap.start()


if __name__ == "__main__":
    c = Controller("input/scratch.wav", "input/reversed.wav")
