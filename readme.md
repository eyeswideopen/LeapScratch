==============================
Leap-Scratch -An In Air Turntable Simulator
==============================
 
ABSTRACT
==============================


Leap-Scratch simulates the behaviour and characteristic audio features of a turntable and a rotating longplayer while manually interact with it - scratching. A rotaing longplayer is simulated in space above a Leap Motion Gusture-Tracking-Controller and the users hand position is analysed to manipulate the played audio information. Furthermore there is the the possibility to modify the master volume and crossfade between to audio streams by specified gestures. Thus users are able to use all features of physical turntables but have a digital and visual simulation.

==============================

REQUIREMENTS/INSTALLATION

Hardware:
-Obviously a LeapMotion controller is required to use the System

Software:

1. Install LeapMotion drivers (https://www.leapmotion.com/setup) 
2. Install port audio (http://www.portaudio.com)
3. Install Python 2.7 (http://www.python.org/getit/) 
4. Install Python Pip Package Manager (http://www.pip-installer.org/en/latest/installing.html)
5. Open a console and navigate to Leap-Scratch directory
6. Install required python packages by using Pip --> pip install -r requirements


==============================

USAGE

There are some different implementations located in src directory:

-scratching module contains a simple scratch implementation without any additional features

start it by navigating to src/scratching and then start the MainController file --> python MainController.py
	

-complete module contains a scratch implementation including additional features like volume and crossfade gesture detection

start it by navigating to src/complete and then start the MainController file --> python MainController.py
	
	
-gui module contains a seperate audio, scratch and leap controller implementations, adjusted to a conceptual gui realisation

start it by navigating to src/gui and then start the MainController file --> python MainController.py



==============================

by Maximilian Körner and Samuel Zeitler