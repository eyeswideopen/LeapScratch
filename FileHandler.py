from __future__ import division
import wave
import audioop
import numpy
import scipy
from scipy import interpolate
from scipy import signal


class FileHandler:
    def __init__(self, fileName):
        self.wf = wave.open(fileName, 'rb')
        self.wf.setpos(3000000)
        self.index = 3000000

    def getAudio(self, frames, scale):

        #TODO: perfektes mass finden
        if abs(scale) < 0.2:
            return (frames * 4) * "0"

        framesToRead = int(frames * abs(scale))

        print framesToRead
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



        length = 4096 / len(smp)

        data = numpy.fromstring(smp, dtype=numpy.int8)

        print data[10]

        #CRAPPY RESAMLER
        ##scipy
        #data = signal.resample(data, 4096)

        ##scikits.samplerate
        #data = sciResample(data, length, 'sinc_best')

        ##numpy 
        # n = round(len(data) * length)
        # data = numpy.interp(
        #     numpy.linspace(0.0, 1.0, n, endpoint=False),
        #     numpy.linspace(0.0, 1.0, len(data), endpoint=False),
        #     data,)
        #print "len data davor: " + str(len(data))


        # Interpolate the data above to the grid defined by "xvec"
        #xvec = numpy.linspace(0.0, len(data)-1, num=4096, endpoint=False)


        x = numpy.arange(len(data))
        xvec = numpy.arange(4096) / len(data)




        #data = interpolate.pchip(x, data, 4096)



        f = interpolate.pchip(x, data)

        ret = numpy.arange(4096)
        for i in ret:
            ret[i] = f(i / len(data))

        return data.astype(numpy.int16).tostring()




        #print "len data danach: " + str(len(ret))
        #return str(ret)


        # Initialize the interpolator slopes
        #m = pychip.pchip_init(x, data)

        # Call the monotonic piece-wise Hermite cubic interpolator
        #data = pychip.pchip_eval(x, data, m, xvec)

        #safety first
        while len(data) < 4096:
            data = data + data[len(data) - 1]

        return data


    def getChannels(self):
        return self.wf.getnchannels()

    def getFramerate(self):
        return self.wf.getframerate()

    def getSampleWidth(self):
        return self.wf.getsampwidth()

    def close(self):
        self.wf.close()