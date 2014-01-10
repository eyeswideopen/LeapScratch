import pyaudio
import struct
import numpy


class AudioController:
    def __init__(self, fileObject, scaleFunction=lambda:1,volumeFunction=lambda:1):

        self.p = pyaudio.PyAudio()
        self.file = fileObject
        self.interpolationBufferTail = [0, 0, 0, 0, 0, 0]

        def callback(in_data, frame_count, time_info, status):
            return self.getAudio(frame_count, scaleFunction(),volumeFunction()), pyaudio.paContinue

        self.stream = self.p.open(format=self.p.get_format_from_width(self.file.getSampleWidth()),
                                  channels=self.file.getChannels(),
                                  rate=self.file.getFramerate(),
                                  output=True,
                                  stream_callback=callback,
                                  frames_per_buffer=512)

    def start(self):
        self.stream.start_stream()


    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


    def getAudio(self, frames, scale,volume):


        #frames is the requested amount of int16 sample per channel
        #means if frames is 1024 we have to return a string containing 2048 samples of interleaved int16 data
        #thus len(data) has to be 4096 as one char is only 1 byte long

        framesToRead = int(frames * abs(scale))

        #to low scale => silence
        if abs(scale) < 0.1:
            return (frames * 4) * "0"

        data = self.file.getFileData(framesToRead, True if scale < 0 else False)

        #append head for interpolation
        data = tuple(self.interpolationBufferTail) + data

        #resample
        if scale!=1:
            data = self.resample(data, frames * 2)


        #save tail for next interpolation
        self.interpolationBufferTail = data[len(data) - 6:]

        data=map(lambda x: x*volume,data)

        return struct.pack("%dh" % (len(data)), *list(data))


    def resample(self, inData, length):


        ##6-point, 5th-order optimal 32x z-form interpolator
        ##params:
        ##x = ranges from 0 to 1. distance between y[2] and point to be interpolated
        ##y = 6 point surrounding array e.g.: y[0] y[1] y[2] <point to be interpolated> y[3] y[4] y[5]

        def waveInterpolator(x, y):
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


        #generating our indices to interpolate at by ignoring our leading and trailing buffers of len 6 each
        interpolationIndices = numpy.linspace(6, len(inData) - 7, num=length)
        #TODO: maybe 2 mehr an laenge nehmen und vorne und hinten abcutten, da die immer exakt drauf liegen...

        ##
        ##hermite interpolation using waveInterpolator
        ##

        #generate params
        outData = []
        for i in interpolationIndices:
            dist = float(i - int(i))
            params = []
            pointer = int(i)

            params.append(inData[pointer - 4])
            params.append(inData[pointer - 2])
            params.append(inData[pointer])
            #between these two points is our index located, distance represented by dist
            params.append(inData[pointer + 2])
            params.append(inData[pointer + 4])
            params.append(inData[pointer + 6])

            outData.append(waveInterpolator(dist, params))





        return outData