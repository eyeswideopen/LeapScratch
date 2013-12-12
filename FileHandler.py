import wave
import audioop
import numpy
from scipy import signal


class FileHandler:
    def __init__(self):
        self.wf = wave.open("output/file.wav", 'rb')
        self.index = 0

    def getAudio(self, frames, scale):

        # print scale

        if abs(scale) < 0.01:
            return (frames * 4) * "0"

        framesToRead = int(frames * abs(scale))


        data = self.readFromFile(framesToRead, True if scale < 0 else False)

        #if scale != 1.0:
        return self.resample(data, abs(scale))

        #return data


    def readFromFile(self, frames, reverse):

        # if reverse sound should be played
        if reverse:
            if self.index - frames < 0:
                self.index = 0
                #TODO: rest laden, umdrehen und mit nullen auffuellen
                return frames * "0"

            self.wf.setpos(self.index - frames)

        data = self.wf.readframes(frames)

        if reverse:
            self.index -= frames
            self.wf.setpos(self.index)
            return audioop.reverse(data, self.getSampleWidth())

        self.index += frames
        return data

    def resample(self, smp, scale=1.0):

        return signal.resample(smp, 4096);

        data = numpy.fromstring(smp, dtype=numpy.int16)

        # scale = 1 / scale
        # print scale * len(smp)
        # n = round(len(smp) * scale)
        #
        # return numpy.interp(
        #     numpy.linspace(0.0, 1.0, n, endpoint=False),
        #     numpy.linspace(0.0, 1.0, len(data), endpoint=False),
        #     data,
        # ).astype(numpy.int16).tostring()

    def getChannels(self):
        return self.wf.getnchannels()

    def getFramerate(self):
        return self.wf.getframerate()

    def getSampleWidth(self):
        return self.wf.getsampwidth()

    def close(self):
        self.wf.close()