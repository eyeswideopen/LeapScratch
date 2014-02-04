from threading import Thread
from fastAudioController import AudioController
from crossfadeLeapController import fastLeapController

class fastController(Thread):
    def __init__(self, baseFilePath,scratchFilePath):
        Thread.__init__(self)
        self.leap = fastLeapController()
        self.baseMusic = AudioController(baseFilePath, volumeFunction=self.leap.getBaseCrossfade)
        self.scratchMusik = AudioController(scratchFilePath, scaleFunction=self.leap.getScale, volumeFunction=self.leap.getScratchCrossfade)
        self.leap.start()

if __name__ == "__main__":
    c = fastController("input/file.wav", "input/scratch.wav")
