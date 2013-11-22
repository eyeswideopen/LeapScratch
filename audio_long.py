from __future__ import division
import wave,audioop,pyaudio,numpy,sys

class Sampler():

    def __init__(self,waveFile):
        self.wave=wave.open(waveFile, 'rb')
        self.audio=pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.audio.get_format_from_width(self.wave.getsampwidth()),
            channels=self.wave.getnchannels(),
            rate=int(self.wave.getframerate()),
            output=True)

        self.savedData=""
        self.savedReversedData=""
        self.index=0


    def resample(self,smp, scale=1.0):

        n = round(len(smp) * scale)

        return numpy.interp(
            numpy.linspace(0.0, 1.0, n, endpoint=False),
            numpy.linspace(0.0, 1.0, len(smp), endpoint=False),
            smp,
            )

    def playPart(self,reverse,scale):

        if (len(self.savedReversedData)==0 and reverse):
            print("LP out of range, underplayed")
            sys.exit(0)

        CHUNK=1024
        inverseScale=1/scale
        frames=CHUNK
        data=0


        if scale<1:
            frames=int(CHUNK*inverseScale)

        if (frames+self.index>self.wave.getnframes()):
            print("LP out of range, overplayed")
            sys.exit(0)


        if not reverse and self.wave.tell()==self.index:
            data=self.wave.readframes(frames)
            self.savedReversedData+=data
            self.savedData=""
            self.index+=frames

        else:

            if reverse:
                ind=len(self.savedReversedData)-frames*4
                data=self.savedReversedData[ind:]
                self.savedReversedData=self.savedReversedData[:ind]
                self.savedData=data+self.savedData
                self.index-=frames
            else:
                ind=frames*4
                data=self.savedData[:ind]
                self.savedData=self.savedData[ind:]
                self.savedReversedData+=data
                self.index+=frames

        if len(data)==0:
            #TODO: why?
            print(reverse,scale)
            return 0

        if reverse:
            data = audioop.reverse(data,self.wave.getsampwidth())


        if scale!=1:

            audio_data = numpy.fromstring(data, dtype=numpy.int16)
            output=self.resample(audio_data,scale)
            string_audio_data=output.astype(numpy.int16).tostring()

        else:
            string_audio_data=data

        for i in range(0,len(string_audio_data),len(data)):
             self.stream.write(string_audio_data[i:i+len(data)])

        return frames

    def play(self,reverse,scale):

        CHUNK = 1024
        index=0
        if reverse:
            index=self.wave.getnframes()-CHUNK
            self.wave.setpos(index)


        while True:
            border=self.playPart(reverse,scale)

            if reverse:
                index-=border
                if index<0:
                    break
                self.wave.setpos(index)
            else:
                index+=border
                if index>=self.wave.getnframes():
                    break


        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

if __name__=="__main__":

    sa=Sampler("output/file.wav")
    #sa.play(False,0.3)
    vectorSpeed=[1 for i in range(1000)]
    vectorSpeed+=[(j/510) for j in range(200,510,5)[::-1]]
    vectorSpeed+=[(k/800) for k in range(200,800,5)]
    vectorSpeed+=[(k/800) for k in range(200,800,5)[::-1]]
    vectorSpeed+=[1 for i in range(1000)]

    # for s in vectorSpeed:
    #     sa.playPart(False,s)

    vectorReverse=[False for i in range(1000)]
    vectorReverse+=[True for i in range(250)]
    vectorReverse+=[False for i in range(250)]
    vectorReverse+=[True for i in range(250)]
    vectorReverse+=[False for i in range(325)]
    vectorReverse+=[True for i in range(500)]


    # for r in vectorReverse:
    #     sa.playPart(r,1)


    for i in range(len(vectorSpeed)):
        sa.playPart(vectorReverse[i],vectorSpeed[i])
