import argparse
import datetime
import imutils
import time
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="min area")
args = vars(ap.parse_args())

# read from webcam if no video
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)

# else read from file
else:
    camera = cv2.VideoCapture(args["video"])

# init first frame
firstFrame = None

# loop over frames
while True:
    (grabbed, frame) = camera.read()
    
    if not grabbed:
        break

    # resize and convert frame
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    # if no first frame, init
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute difference
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate image and find contours
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over contours
    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # bounding box of changed frame
        (x,y,w,h) = cv2.boundingRect(c)

        # show and record frame
        #cv2.imshow("Person Detected", frame)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Frame Delta", frameDelta)

        # save image to file
        cv2.imwrite("detected.png", frameDelta)



