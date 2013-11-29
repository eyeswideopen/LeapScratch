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
        self.length=self.wave.getnframes()
        self.sampleWidth=self.wave.getsampwidth()

    def resample(self,smp, scale=1.0):

        n = round(len(smp) * scale)

        return numpy.interp(
            numpy.linspace(0.0, 1.0, n, endpoint=False),
            numpy.linspace(0.0, 1.0, len(smp), endpoint=False),
            smp,
            )

    def playPart(self,reverse,scale):
        if self.index>=self.length:
            print("LP out of range, overplayed")
            sys.exit(0)
        elif self.index<=0 and reverse:
            print("LP out of range, underplayed")
            sys.exit(0)

        CHUNK=1024
        inverseScale=1/scale
        frames=CHUNK
        data=0
        pointer=self.wave.tell()

        if scale<1:
            frames=int(CHUNK*inverseScale)

        #read frames, required data is not in memory yet
        if not reverse and pointer<=self.index:
            #clearing dispensable bytes from index, caused by overrunning increment of index
            if self.index>pointer:
                self.index=pointer
            data=self.wave.readframes(frames)
            self.savedReversedData+=data
            self.savedData=""
            self.index+=frames

        #required data has been already played and is stored in memory
        else:
            if reverse:
                ind=len(self.savedReversedData)-frames*4
                audio_data=self.savedReversedData[ind:]
                data=audioop.reverse(audio_data,self.sampleWidth)
                self.savedReversedData=self.savedReversedData[:ind]
                self.savedData=audio_data+self.savedData
                self.index-=frames
            else:
                ind=frames*4
                data=self.savedData[:ind]
                self.savedData=self.savedData[ind:]
                self.savedReversedData+=data
                self.index+=frames

        #resample data if any scale is given
        if scale!=1:
            audio_data = numpy.fromstring(data, dtype=numpy.int16)
            output=self.resample(audio_data,scale)
            string_audio_data=output.astype(numpy.int16).tostring()
        else:
            string_audio_data=data

        #iterate over string_audio_data and write 4096 byte into stream for each iteration
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
    sa.play(False,0.25)


    vectorSpeed=[0.75 for i in range(2000)]
    vectorSpeed+=[(j/50) for j in range(1,50,10)[::-1]]
    vectorSpeed+=[(k/100) for k in range(1,200,12)]
    vectorSpeed+=[0.75 for i in range(200)]
    vectorSpeed+=[(k/100) for k in range(1,150,12)]
    vectorSpeed+=[150/100 for i in range(500)]
    vectorSpeed+=[(k/800) for k in range(200,700,5)[::-1]]
    vectorSpeed+=[(k/800) for k in range(1,800,5)]
    vectorSpeed+=[(k/800) for k in range(200,700,5)[::-1]]
    vectorSpeed+=[(k/800) for k in range(1,800,5)]
    vectorSpeed+=[(k/800) for k in range(200,700,5)[::-1]]
    vectorSpeed+=[(k/800) for k in range(1,800,5)]
    vectorSpeed+=[(k/800) for k in range(200,700,5)[::-1]]
    vectorSpeed+=[(k/800) for k in range(1,800,5)]
    vectorSpeed+=[(k/800) for k in range(200,700,5)[::-1]]
    vectorSpeed+=[1 for i in range(300)]

    # for s in vectorSpeed:
    #     sa.playPart(False,s)

    vectorReverse=[False for i in range(1000)]
    vectorReverse+=[True for i in range(100)]
    vectorReverse+=[False for i in range(500)]
    vectorReverse+=[True for i in range(750)]
    vectorReverse+=[False for i in range(500)]
    vectorReverse+=[False for i in range(500)]
    vectorReverse+=[True for i in range(750)]
    vectorReverse+=[False for i in range(500)]
    vectorReverse+=[False for i in range(500)]
    vectorReverse+=[True for i in range(750)]
    vectorReverse+=[False for i in range(500)]

    # for r in vectorReverse:
    #     sa.playPart(r,1)


    # speedCounter=0
    # reverseCounter=0
    # while True:
    #     if speedCounter>=len(vectorSpeed):
    #         speedCounter=0
    #     if reverseCounter>=len(vectorReverse):
    #         reverseCounter=0
    #
    #     sa.playPart(vectorReverse[reverseCounter],vectorSpeed[speedCounter])
    #     reverseCounter+=1
    #     speedCounter+=1