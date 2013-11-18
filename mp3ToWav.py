#requirement ffmpeg, pydub

from pydub import AudioSegment
sound = AudioSegment.from_mp3("input/test.mp3")
sound.export("output/file.wav", format="wav")
