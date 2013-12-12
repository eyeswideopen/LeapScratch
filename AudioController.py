import pyaudio

class AudioController:
    def __init__(self,fileObject,scaleMethod):
        self.p = pyaudio.PyAudio()
        self.file=fileObject

        def callback(in_data, frame_count, time_info, status):
            scale=scaleMethod()
            return self.file.getAudio(frame_count,scale), pyaudio.paContinue

        self.stream = self.p.open(format=self.p.get_format_from_width(self.file.getSampleWidth()),
                                  channels=self.file.getChannels(),
                                  rate=self.file.getFramerate(),
                                  output=True,
                                  stream_callback=callback)

    def start(self):
        self.stream.start_stream()


    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


if __name__=="__main__":
    lp = AudioController()
    lp.play()
