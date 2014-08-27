#!/usr/bin/env python

#
#  you'll require https://github.com/bennoleslie/pexif.git
#  for exif data manipulation
#

import cv
import sys
import pexif

files = sys.argv[1:]
capture_step = int(sys.argv[2])


for f in files:
    capture = cv.CaptureFromFile(f)
    print capture

    width = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)
    height = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)
    fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
    frame_count =  cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT)

    for i in xrange(int(frame_count)):
        frame = cv.QueryFrame(capture)
        if frame and (i % capture_step == 0):
            sys.stdout.write('saving frame:%s\r'%i)
            sys.stdout.flush()
            cv.SaveImage("%s.jpg"%(i), frame)
            img = pexif.JpegFile.fromFile("%s.jpg"%(i))
            img.add_exif()