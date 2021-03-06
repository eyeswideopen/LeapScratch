import sys,os

from pydub import AudioSegment

filename=None
exportName=None

try:
	filename=sys.argv[1]
	exportName=sys.argv[2]
except Exception:
	pass

if not exportName:
    print ("no export name given, 'default.wav' will be chosen")
    exportName="default.wav"
elif not exportName.endswith(".wav"):
    exportName+=".wav"


if not filename or not filename.endswith(".mp3") or not os.path.isfile(filename) :
    print("please pass a mp3 file to convert")
    sys.exit(0)

try:
    sound = AudioSegment.from_mp3(filename)
    sound.export("../../input/"+exportName, format="wav")

except Exception as e:
    s= "an error occured"
    if e.message:
        s+=": "+e.message
    print s
    sys.exit(0)

