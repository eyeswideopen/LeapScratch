from __future__ import division
import wave, audioop, pyaudio, numpy, sys, time


class Sampler():
    def __init__(self, waveFile,):
        self.wave = wave.open(waveFile, 'rb')
        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(format=self.audio.get_format_from_width(self.wave.getsampwidth()),
                                      channels=self.wave.getnchannels(),
                                      rate=int(self.wave.getframerate()),
                                      output=True,
                                      stream_callback=self.callback)

        self.savedData = ""
        self.savedReversedData = ""
        self.index = 0
        self.length = self.wave.getnframes()
        self.sampleWidth = self.wave.getsampwidth()

        self.reverse=False
        self.scale=1



    def callback(self, in_data, frame_count, time_info, status):

        if self.scale!=1:
            print("NOT ONE " +str(self.scale))
        # if self.scale>5 or self.scale<0.001:
        #     return "", pyaudio.paContinue

        if self.index >= self.length:
            print("LP out of range, overplayed")
            sys.exit(0)
        elif self.index <= 0 and self.reverse:
            print("LP out of range, underplayed")
            sys.exit(0)

        CHUNK = 1024
        inverseScale = 1 / self.scale
        frames = CHUNK

        data = 0
        pointer = self.wave.tell()

        if self.scale < 1:
            frames = int(CHUNK * inverseScale)

        #read frames, required data is not in memory yet
        if not self.reverse and pointer <= self.index:
            #clearing dispensable bytes from index, caused by overrunning increment of index
            if self.index > pointer:
                self.index = pointer
            data = self.wave.readframes(frames)
            self.savedReversedData += data
            self.savedData = ""
            self.index += frames

        #required data has been already played and is stored in memory
        else:
            if self.reverse:
                ind = len(self.savedReversedData) - frames * 4
                audio_data = self.savedReversedData[ind:]
                data = audioop.reverse(audio_data, self.sampleWidth)
                self.savedReversedData = self.savedReversedData[:ind]
                self.savedData = audio_data + self.savedData
                self.index -= frames
            else:
                ind = frames * 4
                data = self.savedData[:ind]
                self.savedData = self.savedData[ind:]
                self.savedReversedData += data
                self.index += frames

        #resample data if any scale is given
        if self.scale != 1:
            audio_data = numpy.fromstring(data, dtype=numpy.int16)
            print(len(data)*self.scale)

            output = self.resample(audio_data, self.scale)
            string_audio_data = output.astype(numpy.int16).tostring()
        else:
            string_audio_data = data

        #iterate over string_audio_data and write 4096 byte into stream for each iteration
        return_data=""
        for i in range(0, len(string_audio_data), 4096):
            return_data+=string_audio_data[i:i + len(data)]

        #return frames


        return return_data, pyaudio.paContinue

    def start(self):
        self.stream.start_stream()

        while self.stream.is_active():
            time.sleep(0.1)

        self.stream.stop_stream()
        self.stream.close()
        self.wave.close()
        self.audio.terminate()


    def resample(self, smp, scale=1.0):

        n = round(len(smp) * scale)

        return numpy.interp(
            numpy.linspace(0.0, 1.0, n, endpoint=False),
            numpy.linspace(0.0, 1.0, len(smp), endpoint=False),
            smp,
        )

if __name__=="__main__":
    sa=Sampler("output/file.wav")
    sa.play(False,0.25)