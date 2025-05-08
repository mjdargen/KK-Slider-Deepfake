# KK Slider Deepfake

Have KK Slider from Animal Crossing record a custom message for your or your friend's special occasion!

_Michael D'Argenio  
mjdargen@gmail.com  
https://dargen.io  
https://github.com/mjdargen  
Created: May 26, 2020  
Revised: January 15, 2021_

Check out this demo video here:  
[![KK Slider Deepfake Demo](https://img.youtube.com/vi/aJIZB_f8QiM/0.jpg)](https://www.youtube.com/watch?v=aJIZB_f8QiM)

This program uses moviepy and pydub to generate video and audio of KK Slider. This program works like https://www.cameo.com/ where you can ask a celebrity to record a custom message for your or your friend's special occasion. This program allows you to request KK Slider to record a custom message for any occasion.

This program uses equalo-official's animalese generator. It has been slightly modified for use in this project. View their project here: https://github.com/equalo-official/animalese-generator

To run this code in your environment, you will need to:

- Install Python 3, ImageMagick, ffmpeg
  - May have to configure moviepy with ImageMagick for your environment
- Install python dependencies - pip3 install -r requirements.txt
  - pip install nltk
  - pip install pydub
  - pip install moviepy[optional]==1.0.3 (previous versions of moviepy cause errors in my environment)

Video demo: https://youtu.be/aJIZB_f8QiM

This program has a lot of dependencies and is very RAM-intensive. I've made this Google Colab Notebook where you can easily run the code using Google's computing resources: https://colab.research.google.com/drive/14d4U6Yhi2APOhDjANS0SeBlKuCNeBTe-?usp=sharing

For a complete walkthrough of how this program works, you can go here: [Instructables Tutorial](https://www.instructables.com/KK-Slider-Deepfake/) or [Hackster Tutorial](https://www.hackster.io/mjdargen/kk-slider-deepfake-931b3d).
