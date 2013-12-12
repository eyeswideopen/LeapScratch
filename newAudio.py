import pyaudio
import time
from FileHandler import FileHandler
#from LeapController import LeapController

class LeapScratch:
    def __init__(self):
        self.file = FileHandler()
        self.p = pyaudio.PyAudio()
        #self.leap = LeapController()

        self.counter = 0
        self.scale = 0.5
        self.increment = 0.01

        def callback(in_data, frame_count, time_info, status):
            self.counter += 1
            self.scale += self.increment

            # if self.counter > 200:
            #     self.increment = -0.01
            # return self.file.getAudio(frame_count, self.scale), pyaudio.paContinue

            return self.file.getAudio(frame_count, 1.0), pyaudio.paContinue

        self.stream = self.p.open(format=self.p.get_format_from_width(self.file.getSampleWidth()),
                                  channels=self.file.getChannels(),
                                  rate=self.file.getFramerate(),
                                  output=True,
                                  stream_callback=callback)

    def play(self):
        self.stream.start_stream()


        #self.leap.start()
        while self.stream.is_active():
            time.sleep(0.1)

        self.stream.stop_stream()
        self.stream.close()
        self.file.close()
        self.p.terminate()


#main
lp = LeapScratch()
lp.play()
