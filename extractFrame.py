#!/usr/bin/env python

#
#  you'll require https://github.com/bennoleslie/pexif.git
#  for exif data manipulation
#

import cv
import sys
import pexif
import argparse
import re

parser = argparse.ArgumentParser(description='Program transforms video into seperate images for use in visual SFM')

parser.add_argument('-file', action="store",
    help='file to transform', 
    dest="files", default=None)

parser.add_argument('-n', action="store",
    help='use only nth image',  
    dest="capture_step", default=1)

#camera focal length example 43.0mm
parser.add_argument('-f', action="store",
    help='the focal length of the camera',  
    dest="focal_length", default=None)

#apeture value of the lens 4.62EV (f/5.0) 
parser.add_argument('-a', action="store",
    help='apeture value of the lens',  
    dest="apeture_value", default=None)

#camera brand name
parser.add_argument('-cb', action="store",
    help='camera brand name', 
    dest="camera_brand", default=None)

#camera brand model
parser.add_argument('-cm', action="store",
    help='camera model',  
    dest="camera_model", default=None)


args = parser.parse_args()

capture_step = int(capture_step)
if capture_step < 1: capture_step = 1

# N = F/D
# N = f number
# F = focal lenght
# D = diameter of lens

def check_apeture_value(val):
    # check if apeture value is ok
    # example input should be
    # 5.00EV (f/2.8)
    if re.search('%d/.%dEV /(f/%d/)',val):
        return True
    return False

def check_focal_value(val):
    # check if focal value is ok
    # example input should be
    # 49.00 mm
    if re.search('%d/.%d mm',val):
        return True
    return False


for f in files:
    capture = cv.CaptureFromFile(f)

    width = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)
    height = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)
    fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
    frame_count =  cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT)
    codec = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FOURCC)

    if capture_step > frame_count: frame_count = frame_count - 1

    for i in xrange(int(frame_count)):
        frame = cv.QueryFrame(capture)
        if frame and (i % capture_step == 0):
            sys.stdout.write('saving frame:%s\r'%i)
            sys.stdout.flush()
            cv.SaveImage("%s.jpg"%(i), frame)
            img = pexif.JpegFile.fromFile("%s.jpg"%(i))
            
            img.exif.primary.ImageWidth = width
            img.exif.primary.ImageHeight = height

            img.exif.primary.Make = camera_brand
            img.exif.primary.Model = camera_model
            
            img.exif.primary.ApertureValue = apeture_value
            img.exif.primary.FocalLength = focal_length

            img.writeFile("%s.jpg"%(i))