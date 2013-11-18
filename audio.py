import scikits.audiolab as audiolab
import scikits.samplerate as samplerate
import pyaudio
import wave


class WaveSampler:

    def __init__(self,originalFile):
        frames, fs, encoder = audiolab.wavread(originalFile)
        audiolab.wavwrite(frames[::-1],'output/reversed.wav',fs)
        self.audio = pyaudio.PyAudio()
        self.originalWave = wave.open(originalFile, 'rb')
        self.reversedWave =wave.open('output/reversed.wav', 'rb')
        self.originalData=self.originalWave.readframes(self.originalWave.getnframes())
        self.reversedData=self.reversedWave.readframes(self.reversedWave.getnframes())



    def playAudio(self,steps=None ,rateMultiplicator=1,reversed=False,continuous=False):

        stream=self.audio.open(format=self.audio.get_format_from_width(self.originalWave.getsampwidth()),
        channels=self.originalWave.getnchannels(),
        rate=int(self.originalWave.getframerate()*rateMultiplicator),
        output=True)

        CHUNK = 1024

        data=None
        start=0

        if reversed:
            data=self.reversedData
            if continuous:
                 start=self.reversedPos*1024/256
        else:
            data = self.originalData
            if continuous:
                start=self.originalPos*1024/256


        if not steps:
            end=len(data)
        else:
            end=start+steps

        print(start,end)
        for i in range(start, end, CHUNK):
            stream.write(data[i:i+CHUNK])
            if reversed:
                self.reversedPos=i/1024*256
                self.originalPos=self.originalWave.getnframes()-(i/1024*256)
            else:
                self.reversedPos=self.originalWave.getnframes()-(i/1024*256)
                self.originalPos=i/1024*256

        stream.stop_stream()
        stream.close()


    def stop(self):
        self.audio.terminate()

    def playPart(self,startChunkDelay,chunks,audioPath,rateMultiplicator=1):
        if audioPath==None:
            raise RuntimeError("no audio wave file given")


        stream = self.audio.open(format=self.audio.get_format_from_width(self.originalWave.getsampwidth()),
            channels=self.originalWave.getnchannels(),
            rate=int(self.originalWave.getframerate()*rateMultiplicator),
            output=True)

        counter=0
        while counter<startChunkDelay:
            wf.readframes(1024)
            counter+=1

        absoluteChunk=chunks*1024;

        while absoluteChunk >=1024:
            data = wf.readframes(1024)
            stream.write(data)
            absoluteChunk-=1024

        stream.stop_stream()
        stream.close()
        p.terminate()



def playPart(startChunkDelay,chunks,audioPath,rateMultiplicator=1):
    if audioPath==None:
        raise RuntimeError("no audio wave file given")


    wf = wave.open(audioPath, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=int(wf.getframerate()*rateMultiplicator),
        output=True)

    counter=0
    while counter<startChunkDelay:
        wf.readframes(1024)
        counter+=1

    absoluteChunk=chunks*1024;

    while absoluteChunk >=1024:
        data = wf.readframes(1024)
        stream.write(data)
        absoluteChunk-=1024

    stream.stop_stream()
    stream.close()
    p.terminate()

def playAudio(audioPath,rateMultiplicator=1):

    if audioPath==None:
        raise RuntimeError("no audio wave file given")

    CHUNK = 1024

    wf = wave.open(audioPath, 'rb')

    p = pyaudio.PyAudio()


    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=int(wf.getframerate()*rateMultiplicator),
        output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()

# def playNew(audioPath,rateMultiplicator=1):
#
#     if audioPath==None:
#         raise RuntimeError("no audio wave file given")
#
#
#     wf = wave.open(audioPath, 'rb')
#
#     frames, fs, encoder = audiolab.wavread('output/file.wav')
#     p = pyaudio.PyAudio()
#
#
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#         channels=wf.getnchannels(),
#         rate=int(wf.getframerate()*rateMultiplicator),
#         output=True)
#
#     chunk=1024
#
#     data=frames[::-1]
#
#     while True:
#         try:
#             stream.write(data[chunk-1024:chunk].tostring())
#             chunk+=1024
#         except Exception as e:
#             print(e)
#             break



def reverseAudio():
    frames, fs, encoder = audiolab.wavread('output/file.wav')
    audiolab.wavwrite(frames[::-1],'output/jojo.wav',fs)

def revert():
    frames, fs, encoder = audiolab.wavread('output/file.wav')
    audiolab.wavwrite(frames,'output/jojo.wav',fs)


def main():
    #reverseAudio()
    #playAudio('output/jojo.wav',5)
    #playPart(6000,500,'output/jojo.wav')
    #playNew('output/file.wav')

    w=WaveSampler("output/file.wav")
    w.playAudio(steps=3000000)
    w.playAudio(reversed=True,continuous=True,steps=100000,rateMultiplicator=4)
    w.playAudio(steps=250000,continuous=True,rateMultiplicator=4)
    w.playAudio(reversed=True,continuous=True,steps=150000,rateMultiplicator=3)
    w.playAudio(steps=750000,continuous=True,rateMultiplicator=2)
    w.playAudio(reversed=True,continuous=True,steps=500000,rateMultiplicator=3)
    w.playAudio(steps=200000,continuous=True,rateMultiplicator=4)
    w.playAudio(reversed=True,continuous=True,steps=450000,rateMultiplicator=4)
    w.playAudio(continuous=True)

    #w.playAudio(rateMultiplicator=1,reversed=True)
if __name__ == "__main__":
    main()