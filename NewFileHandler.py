from __future__ import  division
import wave
import audioop
import numpy
import time
import scipy
from scipy import interpolate
from scipy import signal


class NewFileHandler:
    def __init__(self,fileName):
        self.wf = wave.open(fileName, 'rb')
        self.wf.setpos(3000000)
        self.index = 3000000

    def getAudio(self, frames, scale):

        #TODO: perfektes mass finden
        if abs(scale) < 0.2:
            return (frames * 4) * "0"

        framesToRead = int(frames * abs(scale))

        #prevent messing up channel order
        if framesToRead % 2 != 0:
            framesToRead += 1

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

    def resample(self, inData):

        #TODO: important! we need 3 more values both for beginning and end frame interpolation! currently using phantom values

        #6-point, 5th-order optimal 32x z-form interpolator
        #params:
        #x = ranges from 0 to 1. distance between y[2] and point to be interpolated
        #y = 6 point surrounding array e.g.: y[0] y[1] y[2] <point to be interpolated> y[3] y[4] y[5]
        def waveInterpolator(x, y):
            offset = 2

            z = x - 1./2.0
            even1 = float(y[offset+1]+y[offset+0])
            odd1 = float(y[offset+1]-y[offset+0])
        
            even2 = float(y[offset+2]+y[offset+-1])
            odd2 = float(y[offset+2]-y[offset+-1])
        
            even3 = float(y[offset+3]+y[offset+-2])
            odd3 = float(y[offset+3]-y[offset+-2])
        
            c0 = float(even1*0.42685983409379380 + even2*0.07238123511170030 + even3*0.00075893079450573)
            c1 = float(odd1*0.35831772348893259 + odd2*0.20451644554758297 + odd3*0.00562658797241955)
            c2 = float(even1*-0.217009177221292431 + even2*0.20051376594086157 + even3*0.01649541128040211)
            c3 = float(odd1*-0.25112715343740988 + odd2*0.04223025992200458 + odd3*0.02488727472995134)
            c4 = float(even1*0.04166946673533273 + even2*-0.06250420114356986 + even3*0.02083473440841799)
            c5 = float(odd1*0.08349799235675044 + odd2*-0.04174912841630993 + odd3*0.00834987866042734)
            return ((((c5*z+c4)*z+c3)*z+c2)*z+c1)*z+c0


        # test that shit!!
        testparams = [1,2,3,5,6,7]
        #print waveInterpolator(0.1, testparams)

        numpyData = numpy.fromstring(inData, numpy.int16)

        print numpyData
        numpyData.astype(numpy.float32)

        ret = numpy.linspace(0, len(numpyData), num=4096, endpoint=False)
        #returnValues = []


        #TODO: FUUUCK whats wrong...

        #fixed usage for 2 interleaved channels
        for i in range(4096):
            #distance to PREVIOUS point
            dist = float(ret[i] - int(ret[i]))
            params = []

            #starting point
            pointer = int(ret[i]) - 4

            for j in range(6):

                #TODO: insert phantom values for start and end
                if pointer < 0 or pointer >= len(numpyData):
                    params.append(1.0)
                    pointer += 2
                    continue

                params.append(numpyData[pointer])
                #print numpyData[pointer]
                pointer += 2

            ret[i] = waveInterpolator(dist, params)

            #returnValues.append(waveInterpolator(dist, params))
        ret.astype(numpy.int16)

        return numpy.array(ret).tostring()


    def getChannels(self):
        return self.wf.getnchannels()

    def getFramerate(self):
        return self.wf.getframerate()

    def getSampleWidth(self):
        return self.wf.getsampwidth()

    def close(self):
        self.wf.close()