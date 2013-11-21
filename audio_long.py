import pyaudio
import wave
import numpy
import audioop

def resample(smp, scale=1.0):

    n = round(len(smp) * scale)

    return numpy.interp(
        numpy.linspace(0.0, 1.0, n, endpoint=False),
        numpy.linspace(0.0, 1.0, len(smp), endpoint=False),
        smp,
        )


reverse=False
scale=5


CHUNK = 1024

wf = wave.open("input/file.wav", 'rb')

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
    inverseScale=1/scale

    data=None
    border=None

    if scale<1:
        frames=int(CHUNK*inverseScale)
        border=frames

        if reverse:
            data = audioop.reverse(wf.readframes(frames),wf.getsampwidth())
        else:
            data=wf.readframes(frames)

        audio_data = numpy.fromstring(data, dtype=numpy.int16)
        output=resample(audio_data,scale)
        string_audio_data=output.astype(numpy.int16).tostring()

        stream.write(string_audio_data)

    elif scale>1:
        border=CHUNK

        if reverse:
            data = audioop.reverse(wf.readframes(CHUNK),wf.getsampwidth())
        else:
            data=wf.readframes(CHUNK)

        audio_data = numpy.fromstring(data, dtype=numpy.int16)
        output=resample(audio_data,scale)
        string_audio_data = output.astype(numpy.int16).tostring()

        for i in range(0,len(string_audio_data),len(data)):
             stream.write(string_audio_data[i:i+len(data)])


    else:
        border=CHUNK
        if reverse:
            data = audioop.reverse(wf.readframes(CHUNK),wf.getsampwidth())
        else:
            data=wf.readframes(CHUNK)
        stream.write(data)


    if reverse:
        index-=border
        if index<0:
            break
        wf.setpos(index)
    else:
        index+=border
        if index>=wf.getnframes():
            break


stream.stop_stream()
stream.close()
p.terminate()


