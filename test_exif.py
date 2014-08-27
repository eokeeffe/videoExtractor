import pexif

img = pexif.JpegFile.fromFile('/home/evan/Pictures/SFM_tests/arc_mouse_model/test5/IMG_0086.JPG')

#print img.get_exif()
print img.dump()
#img.add_exif()

print "All Done"