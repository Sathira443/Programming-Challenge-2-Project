import cv2
import numpy as np

cap = cv2.VideoCapture("los_angeles.mp4")

while True:
    _, frame = cap.read()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

#Testing
#hello
#hello2
#bari na

# my name is sahan