from __future__ import division
import sys
#mac scipy version glitch fix
sys.path.insert(1, "/Library/Python/2.7/site-packages")
import wave
import audioop


class NewFileHandler:
    def __init__(self, fileName):
        self.wf = wave.open(fileName, 'rb')
        self.index = 0
        # self.scale = 1.0

        print "loading file..."
        self.fileData = self.wf.readframes(self.wf.getnframes())
        self.wf.close()
        print len(self.fileData)


    def getFileData(self, frames, reverse):

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