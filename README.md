videoExtractor
==============

simple script and library for extracting images from video file and adding exif data to the extracted images

There are two ways of doing this, either input the individual values as command line arguements or pass an image from the camera that has exif data that will be mirrored in the extracted video images

extractFrame.py is the manual script that requires a video file and cmd args to work

extractFrameAuto.py is the automated script, needs a video file and image to work

extractFrameAuto_Calibrate.py is the automated script that will undistort image as well
as add EXIF information from video images

python extractFrame.py -h will display the arguements you need for input

If you don't have the required libraries to run this, try the installer script

Tested and Verified on Ubuntu 14.04 LTS
