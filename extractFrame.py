#!/usr/bin/env python

#
#  make sure to run install.sh before trying this script
#  for exif data manipulation
#

import cv
from gi.repository import GExiv2
from fractions import Fraction
import argparse,re,time,os,sys
import random,math


parser = argparse.ArgumentParser(description='Program transforms video into seperate images for use in visual SFM')

parser.add_argument('-file', action="store",
    help='file to transform', 
    dest="files", default=None)

parser.add_argument('-n', action="store",
    help='use only nth image',  
    dest="capture_step", default=1)

#camera focal number example f(1/8)
parser.add_argument('-fnumber', action="store",
    help='the focal number of the camera',  
    dest="fnumber", default=None)

#camera focal length example 43.0mm
parser.add_argument('-focal', action="store",
    help='the focal length of the camera',  
    dest="focal_length", default=None)

#aperture value of the lens 4.62EV (f/5.0) 
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

capture_step = int(args.capture_step)
if capture_step < 1: capture_step = 1

tf = ''.join(args.files)
files = []
for f in tf.split(' '):
    files.append(f.split(','))

fnumber = args.fnumber
focal_length = args.focal_length
apeture_value = args.apeture_value
camera_model = args.camera_model
camera_brand = args.camera_brand

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

def check_focal(val):
    if(re.search("(m|M){2}",val)):
        return val
    else:
        return str(val+"mm")

files = [item for sublist in files for item in sublist]
print "Converting files:",files

print "values:"
print "FNumber:",fnumber
print "Focal Length:",focal_length
print "Aperture Value:",apeture_value
print "Camera Model:",camera_model
print "Camera Brand:",camera_brand

for f in files:
    capture = cv.CaptureFromFile(f)

    width = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)
    height = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)
    fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
    frame_count =  cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT)
    codec = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FOURCC)

    print "Starting work on %s now" % f

    if capture_step > frame_count: frame_count = frame_count - 1

    ISOSPEEDS = [64, 100, 200, 250, 320, 400, 640, 800, 1000, 1600, 3200]
    SHUTTERSPEEDS = [15, 30, 60, 125, 250, 400, 500, 1000, 1250, 1600, 2000, 4000]
    FSTOPS = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3.2, 3.4, 3.7, 4, 4.4, 4.8, 5.2, 5.6, 6.2, 6.7, 7.3, 8, 8.7, 9.5, 10, 11, 12, 14, 15, 16, 17, 19, 21, 22]
    
    flash = [0x00, 0x1, 0x18, 0x19, 0x49, 0x4d, 0x4f, 0x49, 0x4d, 0x4f]
    aperture = Fraction(random.uniform(1.0, 16.0)).limit_denominator(2000)
    exposure = Fraction(1.0/round(random.randint(8, int(100.0*aperture))+1, -2)).limit_denominator(4000)
    
    for i in xrange(int(frame_count)):
        frame = cv.QueryFrame(capture)
        if frame and (i % capture_step == 0):
            sys.stdout.write('saving frame:%s\r'%i)
            sys.stdout.flush()
            path = "%s.jpg"%(i)
            cv.SaveImage(path, frame)
           
            exif = GExiv2.Metadata(path)
            
            t = os.path.getctime(path)
            ctime = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(t))

            exif['Exif.Image.ImageDescription'] = "SEQ#%s"%i
            exif['Exif.Image.Make'] = camera_brand
            exif['Exif.Image.Model'] = camera_model
            exif['Exif.Image.DateTime'] = ctime
            exif['Exif.Image.Software'] = "https://github.com/eokeeffe/videoExtractor"
            
            exif['Exif.Photo.UserComment'] = "awesomeness"


            exif['Exif.Photo.Flash'] = str(flash[0])
            exif['Exif.Photo.FNumber'] = str(Fraction(math.pow(1.4142, aperture)).limit_denominator(2000))
            exif['Exif.Photo.FocalLength'] = str(focal_length)
            exif['Exif.Photo.ApertureValue'] = str(aperture)
            exif['Exif.Photo.ExposureTime'] = str(exposure)
            exif['Exif.Photo.ExposureBiasValue'] = "0 EV"
            exif['Exif.Photo.ISOSpeedRatings'] = "50"
            exif['Exif.Image.Orientation'] = str(0)

            # camera_brand
            # camera_model

            exif.save_file()