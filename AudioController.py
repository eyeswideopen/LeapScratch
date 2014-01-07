import pyaudio
import struct
import numpy


class BaseAudioController:
    def __init__(self, fileObject, volumeFunction=lambda: 1, createStream=True):
        #
        #pyaudio variables
        #
        self.p = pyaudio.PyAudio()
        self.file = fileObject

        if createStream:
            def callback(in_data, frame_count, time_info, status):
                return self.getAudio(frame_count, volume=volumeFunction()), pyaudio.paContinue

            self.stream = self.p.open(format=self.p.get_format_from_width(self.file.getSampleWidth()),
                                      channels=self.file.getChannels(),
                                      rate=self.file.getFramerate(),
                                      output=True,
                                      stream_callback=callback,
                                      frames_per_buffer=1024)


    def start(self):
        self.stream.start_stream()


    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


    def getAudio(self, frames, scale=1, volume=1):
        #frames is the requested amount of int16 sample per channel
        #means if frames is 1024 we have to return a string containing 2048 samples of interleaved int16 data
        #thus len(data) has to be 4096 as one char is only 1 byte long

        # if abs(scale) < 0.1:
        #     return (frames * 4) * "0"

        framesToRead = frames

        data = self.file.getFileData(framesToRead)

        #1 short out of each 2 chars in data
        count = len(data) / 2
        format = "%dh" % (count) #results in '2048h' as format: 2048 short

        #interleaved int16 data of both channels with #frames samples
        shorts = struct.unpack(format, data)

        audioData = map(lambda x: x * volume, shorts)

        return struct.pack("%dh" % (len(audioData)), *list(audioData))


class ScratchAudioController(BaseAudioController):
    def __init__(self, fileObject, volumeFunction=lambda: 1, scaleFunction=lambda: 1):

        BaseAudioController.__init__(self, fileObject, createStream=False)

        #
        #audio manipulation variables
        #
        self.leftInterpolationBuffer = [0, 0, 0]
        self.rightInterpolationBuffer = [0, 0, 0]


        def callback(in_data, frame_count, time_info, status):
            return self.getAudio(frame_count, volume=volumeFunction(), scale=scaleFunction()), pyaudio.paContinue

        self.stream = self.p.open(format=self.p.get_format_from_width(self.file.getSampleWidth()),
                                  channels=self.file.getChannels(), rate=self.file.getFramerate(), output=True,
                                  stream_callback=callback, frames_per_buffer=1024)


    def getAudio(self, frames, volume=1, scale=1):

        #frames is the requested amount of int16 sample per channel
        #means if frames is 1024 we have to return a string containing 2048 samples of interleaved int16 data
        #thus len(data) has to be 4096 as one char is only 1 byte long

        # if abs(scale) < 0.1:
        #     return (frames * 4) * "0"

        framesToRead = int(frames * abs(scale))

        #prevent messing up channel order
        if framesToRead % 2 != 0:
            framesToRead += 1

        if abs(scale) < 0.1:
            data = (frames * 4) * "0"
        else:
            data = self.file.getFileData(framesToRead, True if scale < 0 else False)

        #1 short out of each 2 chars in data
        count = len(data) / 2
        format = "%dh" % (count) #results in '2048h' as format: 2048 short

        #interleaved int16 data of both channels with #frames samples
        shorts = struct.unpack(format, data)

        #
        # MODIFICATION OF INTERLEAVED SAMPLES
        #

        # deinterleaving
        leftChannel = shorts[::2]
        rightChannel = shorts[1::2]


        #
        # MODIFICATION AFTER DEINTERLEAVING FOR INDEPENDANT CHANNEL ALTERATION
        #




        leftChannel = self.resample(leftChannel, frames, self.leftInterpolationBuffer)
        rightChannel = self.resample(rightChannel, frames, self.rightInterpolationBuffer)

        leftChannel=map(lambda xl: xl*volume,leftChannel)
        rightChannel=map(lambda xr: xr*volume,rightChannel)

        #save last 3 played frames for next interpolation
        self.leftInterpolationBuffer = leftChannel[len(leftChannel) - 3:]
        self.rightInterpolationBuffer = rightChannel[len(leftChannel) - 3:]


        #interleave channels back together!
        interleaved = numpy.vstack((leftChannel, rightChannel)).reshape((-1,), order='F')

        return struct.pack("%dh" % (len(interleaved)), *list(interleaved))


    def resample(self, inData, length, interpolationBufferTail):

        ##6-point, 5th-order optimal 32x z-form interpolator
        ##params:
        ##x = ranges from 0 to 1. distance between y[2] and point to be interpolated
        ##y = 6 point surrounding array e.g.: y[0] y[1] y[2] <point to be interpolated> y[3] y[4] y[5]
        def waveInterpolator(x, y):
            z = x - 1. / 2.0
            even1 = float(y[1] + y[0])
            odd1 = float(y[1] - y[0])

            even2 = float(y[2] + y[-1])
            odd2 = float(y[2] - y[-1])

            even3 = float(y[3] + y[-2])
            odd3 = float(y[3] - y[-2])

            c0 = float(even1 * 0.42685983409379380 + even2 * 0.07238123511170030 + even3 * 0.00075893079450573)
            c1 = float(odd1 * 0.35831772348893259 + odd2 * 0.20451644554758297 + odd3 * 0.00562658797241955)
            c2 = float(even1 * -0.217009177221292431 + even2 * 0.20051376594086157 + even3 * 0.01649541128040211)
            c3 = float(odd1 * -0.25112715343740988 + odd2 * 0.04223025992200458 + odd3 * 0.02488727472995134)
            c4 = float(even1 * 0.04166946673533273 + even2 * -0.06250420114356986 + even3 * 0.02083473440841799)
            c5 = float(odd1 * 0.08349799235675044 + odd2 * -0.04174912841630993 + odd3 * 0.00834987866042734)
            return ((((c5 * z + c4) * z + c3) * z + c2) * z + c1) * z + c0


        interpolationIndices = numpy.linspace(0, len(inData) - 4,
                                              num=length) #-4 because we use the last 3 values as phantom values


        ##
        ##hermite interpolation using waveInterpolator
        ##

        for i in range(length):
            #distance to PREVIOUS point
            dist = float(interpolationIndices[i] - int(interpolationIndices[i]))
            params = []

            #starting point
            pointer = int(interpolationIndices[i]) - 2

            for j in range(6):

                #take saved buffer tail phantom values
                if pointer < 0:
                    params.append(interpolationBufferTail[3 + pointer])
                    pointer += 1
                    continue

                if pointer >= len(inData):
                    print "shit"
                    params.append(1.0)
                    pointer += 1
                    continue

                params.append(inData[pointer])
                #print numpyData[pointer]
                pointer += 1

            interpolationIndices[i] = waveInterpolator(dist, params)
        return interpolationIndices


