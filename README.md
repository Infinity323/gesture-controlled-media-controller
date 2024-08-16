# Gesture-Controlled Media Controller

Authors: Paul Lee, Hamza Syed

## Summary

This project allows the user to map their infrared-controlled device's functions to hand gestures that can be performed in front of the camera.

It also supports the operation of multiple remotes, depending on which one is selected as "active."

## Setup Instructions

Must have Debian 10 "buster" 32-bit OS installed on Raspberry Pi.

Run the following commands:

* Install FFmpeg and OpenCV

```sudo apt install ffmpeg python3-opencv python3-pip```

* Install dependency packages

```sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23```

* Install additional dependencies (jpeg)

```sudo apt-get install libjpeg-dev zlib1g-dev```

* Install MediaPipe

```sudo pip3 install mediapipe-rpi4```

Do `mediapipe-rpi3` instead if you have a Raspberry Pi 3

<https://pypi.org/project/mediapipe-rpi4/>

* Install IRSlinger for remote control

<https://github.com/bschwind/ir-slinger>
