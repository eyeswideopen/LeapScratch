
#Leap-Scratch


##An In Air Turntable Simulator




Leap-Scratch simulates the behaviour and characteristic audio features of a turntable and a rotating longplayer while manually interact with it - scratching. A rotaing longplayer is simulated in space above a Leap Motion Gusture-Tracking-Controller and the users hand position is analysed to manipulate the played audio information. Furthermore there is the the possibility to modify the master volume and crossfade between to audio streams by specified gestures. Thus users are able to use all features of physical turntables but have a digital and visual simulation.

==============================



###REQUIREMENTS/INSTALLATION


Hardware:

- Obviously a **LeapMotion** controller is required to use the system
- Another trivial requirement is an **audio speaker** installation 
- Audio de-interleaving, re-sampling and re-interleaving is **pretty costly**. Low RAM and/or processor resources may cause sound flickering.
- The system is **cross-platform**. Therefore you can use LeapScratch on Linux, Windows and MacOSX machines.


Software:

1. Install LeapMotion drivers (https://www.leapmotion.com/setup) 
2. Download, build and install port audio (http://www.portaudio.com)
3. Install Python 2.7 (http://www.python.org/getit/) 
4. Install PyAudio, a python wrapper for portaudio (http://people.csail.mit.edu/hubert/pyaudio/)
5. Install Python Pip Package Manager (http://www.pip-installer.org/en/latest/installing.html)
6. Open a console and navigate to Leap-Scratch directory
7. Install required python packages by using Pip: <pre><code>pip install -r requirements</pre></code>


==============================



###USAGE


There are some different implementations located in src directory:

- **scratching** module contains a simple scratch implementation without any additional features. Code is located in **src/scratching**.

- **complete** module contains a scratch implementation including additional features like volume and cross-fade gesture detection. Code is located in **src/complete**.
	
- **gui** module contains a separate audio, scratch and leap controller implementations, adjusted to a conceptual gui realisation.  Code is located in **src/gui**.


Start the particular module by navigating to respective directory and start the MainController file: <pre><code>python MainController.py</pre></code>

You can select own audio files for the base and scratch streams by editing the "config" file in root project directory. Files must be located in "input" directory! 


==============================



###CONVERTER


If you want to use the embedded mp3-to-wave **converter**, you have to install ffmpeg on your machine (http://www.ffmpeg.org/download.html). Additionally the python library pydub is required. Use "pip install pydub"!

usage:

<pre><code>python mp3ToWav.py \<path/to/input/mp3/file\> [output name]</pre></code>

example: <pre><code>python mp3ToWav.py '/home/user1/file.mp3' 'output.wav' </pre></code>

==============================



###DOCUMENTATION

Product video: http://www.youtube.com/watch?v=ZENE0FXjj94

Please have a look at **doc** directory for further information!

==============================

by Maximilian Koerner and Samuel Zeitler