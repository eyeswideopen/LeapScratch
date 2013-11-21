import pyaudio
import wave

try:
    import scikits.audiolab as audiolab
except Exception:
    pass

import numpy
import audioop

def resample(smp, scale=1.0):
    """Resample a sound to be a different length

    Sample must be mono.  May take some time for longer sounds
    sampled at 44100 Hz.

    Keyword arguments:
    scale - scale factor for length of sound (2.0 means double length)

    """
    # f*ing cool, numpy can do this with one command
    # calculate new length of sample
    n = round(len(smp) * scale)
    # use linear interpolation
    # endpoint keyword means than linspace doesn't go all the way to 1.0
    # If it did, there are some off-by-one errors
    # e.g. scale=2.0, [1,2,3] should go to [1,1.5,2,2.5,3,3]
    # but with endpoint=True, we get [1,1.4,1.8,2.2,2.6,3]
    # Both are OK, but since resampling will often involve
    # exact ratios (i.e. for 44100 to 22050 or vice versa)
    # using endpoint=False gets less noise in the resampled sound
    return numpy.interp(
        numpy.linspace(0.0, 1.0, n, endpoint=False), # where to interpret
        numpy.linspace(0.0, 1.0, len(smp), endpoint=False), # known positions
        smp, # known data points
        )



reverse=True
scale=2
CHUNK = 1024

wf = wave.open("output/file.wav", 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(),
    rate=int(wf.getframerate()),
    output=True)

index=0
if reverse:
    index=wf.getnframes()-CHUNK
    wf.setpos(index)


while True:
    data=None
    if scale!=1:
        if reverse:
            data = audioop.reverse(wf.readframes(CHUNK),wf.getsampwidth())
        else:
            data=wf.readframes(CHUNK)

        audio_data = numpy.fromstring(data, dtype=numpy.int16)
        output=resample(audio_data,scale)
        string_audio_data = output.astype(numpy.int16).tostring()

        data=string_audio_data

    else:
        data=None
        if reverse:
            data = audioop.reverse(wf.readframes(CHUNK),wf.getsampwidth())
        else:
            data=wf.readframes(CHUNK)

    stream.write(data)
    if reverse:
        index-=CHUNK
        if index<0:
            break
        wf.setpos(index)
    elif index>=wf.getnframes():
        break


stream.stop_stream()
stream.close()
p.terminate()


# class WaveSampler:
#
#     def __init__(self,originalFile):
#         frames, fs, encoder = audiolab.wavread(originalFile)
#         audiolab.wavwrite(frames[::-1],'output/reversed.wav',fs)
#         self.audio = pyaudio.PyAudio()
#         self.file=originalFile
#         self.originalWave = wave.open(originalFile, 'rb')
#         self.reversedWave =wave.open('output/reversed.wav', 'rb')
#         self.originalData=self.originalWave.readframes(self.originalWave.getnframes())
#         self.reversedData=self.reversedWave.readframes(self.reversedWave.getnframes())
#
#
#     def playSomething(self):
#         d=numpy.fromstring(self.originalData,dtype=numpy.int16)
#         e=resample(d,0.2)
#
#         data=e.astype(numpy.int16).tostring()
#
#         #data=self.originalData
#
#         stream=self.audio.open(format=self.audio.get_format_from_width(self.originalWave.getsampwidth()),
#         channels=self.originalWave.getnchannels(),
#         rate=int(self.originalWave.getframerate()),
#         output=True)
#
#
#         chunk=1024
#
#         print(len(data),len(self.originalData))
#
#         for i in range(0,len(data),chunk):
#             stream.write(data[i:i+chunk])
#
#
#     def playAudio(self,steps=None ,rateMultiplicator=1,reversed=False,continuous=False):
#
#         stream=self.audio.open(format=self.audio.get_format_from_width(self.originalWave.getsampwidth()),
#         channels=self.originalWave.getnchannels(),
#         rate=int(self.originalWave.getframerate()*rateMultiplicator),
#         output=True)
#
#         CHUNK = 1024
#
#         data=None
#         start=0
#
#         if reversed:
#             data=self.reversedData
#             if continuous:
#                  start=self.reversedPos*1024/256
#         else:
#             data = self.originalData
#             if continuous:
#                 start=self.originalPos*1024/256
#
#
#         if not steps:
#             end=len(data)
#         else:
#             end=start+steps
#
#         print(start,end)
#         for i in range(start, end, CHUNK):
#             stream.write(data[i:i+CHUNK])
#             if reversed:
#                 self.reversedPos=i/1024*256
#                 self.originalPos=self.originalWave.getnframes()-(i/1024*256)
#             else:
#                 self.reversedPos=self.originalWave.getnframes()-(i/1024*256)
#                 self.originalPos=i/1024*256
#
#         stream.stop_stream()
#         stream.close()
#
#
#     def stop(self):
#         self.audio.terminate()
#
#
#
#     def playResampled(self):
#
#         class Enes(audiotools.player.AudioOutput):
#             pass
#
#         a=audiotools.open(self.file)
#
#
#         p=audiotools.player.Player(a)
#         p.play()
#         resampler = audiotools.resample.Resampler(2, float(44100) / float(88200), 0)
#
#
#
#
#
# def playPart(startChunkDelay,chunks,audioPath,rateMultiplicator=1):
#     if audioPath==None:
#         raise RuntimeError("no audio wave file given")
#
#
#     wf = wave.open(audioPath, 'rb')
#
#     p = pyaudio.PyAudio()
#
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#         channels=wf.getnchannels(),
#         rate=int(wf.getframerate()*rateMultiplicator),
#         output=True)
#
#     counter=0
#     while counter<startChunkDelay:
#         wf.readframes(1024)
#         counter+=1
#
#     absoluteChunk=chunks*1024;
#
#     while absoluteChunk >=1024:
#         data = wf.readframes(1024)
#         stream.write(data)
#         absoluteChunk-=1024
#
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#
# def playAudio(audioPath,rateMultiplicator=1):
#
#     if audioPath==None:
#         raise RuntimeError("no audio wave file given")
#
#     CHUNK = 1024
#
#     wf = wave.open(audioPath, 'rb')
#
#     p = pyaudio.PyAudio()
#
#
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#         channels=wf.getnchannels(),
#         rate=int(wf.getframerate()*rateMultiplicator),
#         output=True)
#
#     data = wf.readframes(CHUNK)
#
#     while data != '':
#         stream.write(data)
#         data = wf.readframes(1024)
#
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#
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
#
#
#
# def reverseAudio():
#     frames, fs, encoder = audiolab.wavread('output/file.wav')
#     audiolab.wavwrite(frames[::-1],'output/jojo.wav',fs)
#
# def revert():
#     frames, fs, encoder = audiolab.wavread('output/file.wav')
#     audiolab.wavwrite(frames,'output/jojo.wav',fs)
#
#
# def main():
#     pass
#     #reverseAudio()
#     #playAudio('output/jojo.wav',5)
#     #playPart(6000,500,'output/jojo.wav')
#     #playNew('output/file.wav')
#
#     #w=WaveSampler("input/file.wav")
#     #w.playResampled()
#     #w.playSomething()
#     # w.playAudio(reversed=True,continuous=True,steps=100000,rateMultiplicator=0.25)
#     # w.playAudio(steps=250000,continuous=True,rateMultiplicator=0.5)
#     # w.playAudio(reversed=True,continuous=True,steps=150000,rateMultiplicator=3)
#     # w.playAudio(steps=750000,continuous=True,rateMultiplicator=2)
#     # w.playAudio(reversed=True,continuous=True,steps=500000,rateMultiplicator=3)
#     # w.playAudio(steps=200000,continuous=True,rateMultiplicator=4)
#     # w.playAudio(reversed=True,continuous=True,steps=450000,rateMultiplicator=4)
#     # w.playAudio(continuous=True)
#
#
#
#     #w.playAudio(rateMultiplicator=1,reversed=True)
# if __name__ == "__main__":
#     main()