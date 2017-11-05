#!/usr/bin/env python
import cv2, sys, smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# Define constants
DEVICE_NUMBER = 1
IMAGE_FILE = "detected_face.jpg"

# Get XML file input
if len(sys.argv) > 1:
    XML_PATH = sys.argv[1]
else:
    print "Error: XML path not defined"
    sys.exit(1)

# Initialize the cascade classifier
faceCascade = cv2.CascadeClassifier(XML_PATH)

# Initialize webcam
vc = cv2.VideoCapture(DEVICE_NUMBER)

# Check if the webcam works
if vc.isOpened():
    # Try to get the first frame
    retval, frame = vc.read()

else:
    # Exit program
    sys.exit(1)

i = 0
faces = []

# if webcam read 
while retval:

    # define frame
    frame_show = frame
        
    if i%5 == 0:

        # convert frame to grayscale and perform detection
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect objects and return array of faces
        faces = faceCascade.detectMultiScale(
                frame,
                scaleFactor=1.2,
                minNeighbors=2,
                minSize=(50,50),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )
        
        print faces
        
        # if at least one face detected
        if len(faces)>0:

            # draw rectangle
            #for (x,y,w,h) in faces:
            #    cv2.rectangle(frame_show, (x,y), (x+w, y+h), (0,0,255),2)

            # save frame as image file
            #cv2.imshow(IMAGE_FILE, frame_show)
            cv2.imwrite(IMAGE_FILE, frame_show)

            # exit
            break

        # read next frame
        retval, frame = vc.read()

        # exit webcam-loop if escape pressed
        if cv2.waitKey(1) == 27:
            break

        i += 1

# send email
msg = MIMEMultipart()
msg.attach(MIMEText("Face detected!"))
msg['Subject'] = "Someone detected"
msg['From'] = "linaro@localhost"
msg['To'] = "<eshresco@gmail.com>"

try:
    f = open(IMAGE_FILE, "rb")
    img = MIMEImage( f.read() )
    f.close()
    msg.attach(img)
except IOError:
    print "Error: cannot find", IMAGE_FILE

# use sendmail
s = smtplib.SMTP('localhost')
s.set_debuglevel(1)
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()

print "Email sent!"
        

