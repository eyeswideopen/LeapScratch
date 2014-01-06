from __future__ import  division
import wave
import audioop
import numpy
from scipy import signal


class FileHandler:
    def __init__(self,fileName):
        self.wf = wave.open(fileName, 'rb')
        self.index = 0

    def getAudio(self, frames, scale):

        #TODO: perfektes mass finden
        if abs(scale) < 0.2:
            return (frames * 4) * "0"

        framesToRead = int(frames * abs(scale))
        data = self.readFromFile(framesToRead, True if scale < 0 else False)

        if scale != 1.0:
            return self.resample(data)
        return data


    def readFromFile(self, frames, reverse):

        # if reverse sound should be played
        if reverse:
            if self.index - frames < 0:
                self.index = 0
                return frames * "0"

            self.wf.setpos(self.index - frames)

        data = self.wf.readframes(frames)

        if reverse:
            self.index -= frames
            self.wf.setpos(self.index)
            return audioop.reverse(data, self.getSampleWidth())

        self.index += frames
        return data

    def resample(self, smp):

        length=4096/len(smp)

        data = numpy.fromstring(smp, dtype=numpy.int16)
        n = round(len(data) * length)

        return numpy.interp(
            numpy.linspace(0.0, 1.0, n, endpoint=False),
            numpy.linspace(0.0, 1.0, len(data), endpoint=False),
            data,
        ).astype(numpy.int16).tostring()


    def getChannels(self):
        return self.wf.getnchannels()

    def getFramerate(self):
        return self.wf.getframerate()

    def getSampleWidth(self):
        return self.wf.getsampwidth()

    def close(self):
        self.wf.close()