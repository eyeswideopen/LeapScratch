from __future__ import division
import sys
#mac scipy version glitch fix
sys.path.insert(1, "/Library/Python/2.7/site-packages")
import wave
import audioop
import struct


class FileHandler:
    def __init__(self, fileName):
        self.index = 0

        self.wf = wave.open(fileName, 'rb')
        print "loading file..."
        self.fileData = self.wf.readframes(self.wf.getnframes())
        self.wf.close()

        #format: 1 short out of each 2 chars in fileData
        #interleaved int16 data of both channels with #frames samples
        #self.fileData = struct.unpack("%dh" % (len(self.fileData) / 2), self.fileData)
        print "file read to memory and converted to int16"


    def getFileData(self, frames, reverse=False):

        #frames is number of frames per channel in int 16
        #so return frames * 2 short from fileData
        #+6 for interpolation buffer at the end
        #*2 also prevents messing up the channel order

        # print "requested frames: " + str(frames)

        frames = frames * 4

        if reverse:
            if self.index - frames < 0:
                print "UNDERPLAYING AUDIO FILE"
                self.index = frames

            self.index = self.index - frames

        data = self.fileData[self.index:self.index + frames]


        if reverse:
            self.index -= frames

            return_data =audioop.reverse(data,self.wf.getsampwidth())

        self.index += frames

        # print "provided frames: " + str(len(data))
        # print "index: " + str(self.index)


        return data



    def OldgetFileData(self, frames, reverse=False):

        #frames is number of frames per channel in int 16
        #so return frames * 2 * 2 string chars from file string
        frames = frames * 4

        # if reverse sound should be played
        if reverse:
            if self.index - frames < 0:
                self.index = 0
                print "UNDERPLAYING AUDIO FILE"
                return frames * "0"

            self.index = self.index - frames

        #read data
        data = self.fileData[self.index:self.index + frames]

        if reverse:
            self.index -= frames
            return audioop.reverse(data, self.getSampleWidth())

        self.index += frames
        return data

    def getChannels(self):
        return self.wf.getnchannels()

    def getFramerate(self):
        return self.wf.getframerate()

    def getSampleWidth(self):
        return self.wf.getsampwidth()

    def close(self):
        self.wf.close()