#!/usr/bin/env python
from skimage.measure import compare_ssim as ssim #structural_similarity as ssim
#import matplotlib.pyplot as plt
import numpy as np
import cv2
import smtplib
import sys

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.MIMEBase import MIMEBase

# Define functions ----------------

# mean square error between images
def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

# compute similarity
def compare_images(imageA, imageB, title):
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    return m,s

# load all images ---------------------
face1 = cv2.imread("image01.jpg", 0)
face2 = cv2.imread("image02.jpg", 0)
face3 = cv2.imread("image03.jpg", 0)

IMAGE_FILE = "detected_face.jpg"
detected = cv2.imread(IMAGE_FILE, 0)

#face1 = cv2.cvtColor(orig1, cv2.COLOR_BGR2GRAY)
#face2 = cv2.cvtColor(orig2, cv2.COLOR_BGR2GRAY)
#face3 = cv2.cvtColor(orig3, cv2.COLOR_BGR2GRAY)

images = ("Elena", face1), ("Jia", face2), ("Aditi", face3)

# main code ----------------------------

# define constants
count = 0
m = 9999999999
s = 0.0
name = images[0][0]
DEVICE_NUMBER = 1 

# Initialize webcam
#vc = cv2.VideoCapture(DEVICE_NUMBER)
cnt = 0

while  cnt <  1000:
    cnt += 1

# Check if the webcam works
#if vc.isOpened():
    # Try to get the first frame
#    retval, frame = vc.read()

#else:
    # Exit program
   # sys.exit(1)

i = 0
faces = []
frame= []

# if webcam read 
#while retval:
while True:
    # define frame
    #frame_show = frame
    #cv2.imshow(IMAGE_FILE, frame_show)
        
    if i%5 == 0:

        # convert frame to grayscale and perform detection
       # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect objects and return array of faces
        for img in range(len(images)):
            #val = compare_images(frame, images[img][1], "Comparison")
            val = compare_images(detected, images[img][1], "comparison") 
            if (val[0] < m and val[1] > s):
                s = val[1]
                m = val[0]
                name = images[img][0] 
            else:
                count = count+1

        if count == 3:
            name = "Unknown person"

        # save frame as image file
        #cv2.imwrite(IMAGE_FILE, frame_show)
        i += 1

        # exit
        break

    break 

        # read next frame
        #retval, frame = vc.read()

         # exit webcam-loop if escape pressed
        #if cv2.waitKey(1) == 27:
        #    break

        
# send email --------------------------
fromaddr = "technica2017test@gmail.com"
toaddr = "an5vq@virginia.edu" 

body = name + " was here!"

msg = MIMEMultipart()
msg['Subject'] = "Someone detected"
msg['From'] = fromaddr
msg['To'] = toaddr

try:
    msg.attach(MIMEText(body, 'plain'))
    f = open("./"+IMAGE_FILE, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((f).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename=%s" %IMAGE_FILE)
    f.close()
    msg.attach(part)
except IOError:
    print "Error: cannot find", IMAGE_FILE

print "Check email!"

# use sendmail
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "Am@zonsux!")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
        

