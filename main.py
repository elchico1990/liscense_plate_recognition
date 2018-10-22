import sys
#sys.path.append('/media/elchico/863AD2223AD20ED5/Users/ARoy/Downloads/XRvision/xr_new')
#import liscence-plate-detection #import * #import liscence_detect
#import * from .vehicle-detection
import cv2
import os
#import sys

if __name__ == '__main__':
    directory = sys.argv[1]+'/images_from_video'

    if not os.path.exists(directory):
        os.makedirs(directory)


    video_file = cv2.VideoCapture(sys.argv[2])
    success = 1
    i = 0
    while (success):
        success,image = video_file.read()
    #filename  =
        cv2.imwrite('%s/%s.png' % (directory,str(i).zfill(6)), image)
        i = i+1
