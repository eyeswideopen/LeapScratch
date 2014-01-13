import pyaudio
import struct
import numpy
import wave


class AudioController:
    def __init__(self, fileName, scaleFunction=lambda:1,volumeFunction=lambda: 1,stoppingFunction=lambda: 1):

        self.p = pyaudio.PyAudio()

        #
        # file reading and conversion
        #
        self.index = 4 # for resampling

        self.scaleFunction=scaleFunction
        self.volumeFunction=volumeFunction
        self.stoppingFunction=stoppingFunction

        self.wf = wave.open(fileName, 'rb')
        print "loading file ..."
        print fileName
        self.fileStringData = self.wf.readframes(self.wf.getnframes())
        self.wf.close()

        #format: 1 short out of each 2 chars in fileData
        #interleaved int16 data of both channels with #frames samples
        self.fileData = struct.unpack("%dh" % (len(self.fileStringData) / 2), self.fileStringData)
        print "... file read to memory and converted to int16!"


        #
        # audio setup
        #
        self.frameSize = 128
        print "starting audio playback with %i channels, %iHz framerate and %i framesize!" \
              % (self.wf.getnchannels(), self.wf.getframerate(), self.frameSize)


    def start(self):
        def callback(in_data, frame_count, time_info, status):

            if self.index+self.frameSize*2>=self.wf.getnframes()*2:
                self.stoppingFunction()
                return self.getAudio(frame_count, self.scaleFunction(),self.volumeFunction()), pyaudio.paAbort

            return self.getAudio(frame_count, self.scaleFunction(),self.volumeFunction()), pyaudio.paContinue


        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  output=True,
                                  stream_callback=callback,
                                  frames_per_buffer=self.frameSize)


    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


    def getAudio(self, frames, scale,volume):
	

        #frames is the requested amount of int16 sample per channel
        #means if frames is 1024 we have to return a string containing 2048 samples of interleaved x-_---int16 data
        #thus len(data) has to be 4096 as one char is only 1 byte long

        framesToRead = int(frames * abs(scale))

        #to low scale => silence
        if abs(scale) < 0.2:
            return (frames * 4) * "0"

        if scale != 1.0:

            #reverse playback
            if scale < 0.0:
                self.index -= int(frames * 2 * abs(scale))
                data=self.resample(frames * 2, scale)[::-1]
                volumeData=map(lambda x:x*volume,data)
                return struct.pack("%dh" % (len(data)), *list(volumeData)) #reversed resampled audio data

            #just resample
            data=self.resample(frames * 2, abs(scale))
            volumeData=map(lambda x:x*volume,data)
            return struct.pack("%dh" % (len(data)), *list(volumeData))

        #just playing with scale=1
        self.index += 2 * frames
        data=self.fileData[self.index - 2 * frames: self.index]
        volumeData=map(lambda x:x*volume,data)
        return struct.pack("%dh" % (len(data)), *list(volumeData))


    def resample(self, length, scale):

        ##6-point, 5th-order optimal 32x z-form interpolator
        ##params:
        ##x = ranges from 0 to 1. distance between y[2] and point to be interpolated
        ##y = 6 point surrounding array e.g.: y[0] y[1] y[2] <point to be interpolated> y[3] y[4] y[5]

        def hermiteInterpolator(x, y):
            offset = 2

            z = x - 1 / 2.0
            even1 = float(y[offset + 1] + y[offset + 0])
            odd1 = float(y[offset + 1] - y[offset + 0])
            even2 = float(y[offset + 2] + y[offset + -1])
            odd2 = float(y[offset + 2] - y[offset + -1])
            even3 = float(y[offset + 3] + y[offset + -2])
            odd3 = float(y[offset + 3] - y[offset + -2])

            c0 = float(even1 * 0.42685983409379380 + even2 * 0.07238123511170030 + even3 * 0.00075893079450573)
            c1 = float(odd1 * 0.35831772348893259 + odd2 * 0.20451644554758297 + odd3 * 0.00562658797241955)
            c2 = float(even1 * -0.217009177221292431 + even2 * 0.20051376594086157 + even3 * 0.01649541128040211)
            c3 = float(odd1 * -0.25112715343740988 + odd2 * 0.04223025992200458 + odd3 * 0.02488727472995134)
            c4 = float(even1 * 0.04166946673533273 + even2 * -0.06250420114356986 + even3 * 0.02083473440841799)
            c5 = float(odd1 * 0.08349799235675044 + odd2 * -0.04174912841630993 + odd3 * 0.00834987866042734)

            return ((((c5 * z + c4) * z + c3) * z + c2) * z + c1) * z + c0


        interpolationLength = int(length * abs(scale))


        #generating our indices to interpolate at by ignoring our leading and trailing buffers of len 6 each
        # interpolationIndices = numpy.linspace(6, len(inData) - 7, num=length)
        interpolationIndices = numpy.linspace(self.index, self.index + interpolationLength, num=length)

        ##
        ##hermite interpolation using waveInterpolator
        ##

        #generate params
        params = [0,0,0,0,0,0]
        outData =[]
        for i in interpolationIndices:
            dist = float(i - int(i))
            pointer = int(i)

            params[0] = (self.fileData[pointer - 4])
            params[1] = (self.fileData[pointer - 2])
            params[2] = (self.fileData[pointer])
            #between these two points is our index located, distance represented by dist
            params[3] = (self.fileData[pointer + 2])
            params[4] = (self.fileData[pointer + 4])
            params[5] = (self.fileData[pointer + 6])

            outData.append(hermiteInterpolator(dist, params))

        if scale > 0.0:
            self.index += interpolationLength
        return outData