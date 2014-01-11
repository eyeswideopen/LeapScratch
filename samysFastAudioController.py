from __future__ import division
from odbc import internalError
import pyaudio
import struct
import numpy,audioop


class AudioController:
    def __init__(self, fileObject, scaleFunction=lambda: 1,volumeFunction=lambda:1):

        self.p = pyaudio.PyAudio()
        self.file = fileObject

        self.leftInterpolationBuffer = [0, 0, 0]
        self.rightInterpolationBuffer = [0, 0, 0]

        def callback(in_data, frame_count, time_info, status):

            data=self.getAudio(frame_count, scaleFunction(),volumeFunction())
            if len(data)>=frame_count*4:
                return data, pyaudio.paContinue
            else:
                return data, pyaudio.paAbort

        self.stream = self.p.open(format=self.p.get_format_from_width(self.file.getSampleWidth()),
                                  channels=self.file.getChannels(),
                                  rate=self.file.getFramerate(),
                                  output=True,
                                  stream_callback=callback,
                                  frames_per_buffer=128)

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

        # audio_data = numpy.fromstring(data, dtype=numpy.int16)
        # output=self.resample(audio_data,1/abs(scale))

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



        leftChannel=[i for i in leftChannel]
        rightChannel=[i for i in rightChannel]





        #resampling
        if scale != 1.0:
            leftChannel = self.resample(leftChannel,frames)
            rightChannel = self.resample(rightChannel,frames)

        #
        #adjust volume to value provided by volumeFunction
        leftChannel = map(lambda xl: xl * volume, leftChannel)
        rightChannel = map(lambda xr: xr * volume, rightChannel)


        #interleave channels back together!
        interleavedScratchData = numpy.vstack((leftChannel, rightChannel)).reshape((-1,), order='F')


        string_data= struct.pack("%dh" % (len(interleavedScratchData)), *list(interleavedScratchData))



        return string_data




    def resample(self, smp, frames):



        try:
            resampled=numpy.interp(
                numpy.linspace(0.0, 1.0, frames, endpoint=False),
                numpy.linspace(0.0, 1.0, len(smp), endpoint=False),
                smp,
            )
        except ValueError:
            resampled=[0 for i in range(int(frames))]
        return resampled

