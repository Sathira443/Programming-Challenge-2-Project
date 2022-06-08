import cv2
import numpy as np
from tracker import *
from object_detection import ObjectDetection

obj_detection = ObjectDetection()

# Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("Temp.mp4")

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

tracking_objects = {}

while True:

    current_frame_centre_point_list = []

    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Extract Region of interest
    roi = frame[500: 800, 10: 1900]
    # roi = np.array([[10, 1000], [10, 800], [450, 500], [1500, 500], [1900, 800], [1900, 1000]], np.int32)
    # region_of_interest = cv2.fillPoly(np.zeros_like(cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)), roi, 255)
    # region_of_interest_image = cv2.bitwise_and(cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY), region_of_interest)

    # 1. Object Detection
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 100:
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            # x, y, w, h = cv2.boundingRect(cnt)
            (class_ids, scores, boxes) = obj_detection.detect(frame)
            for box in boxes:
                x, y, w, h = box
                # Surround vehicle by a green box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            detections.append([x, y, w, h])

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("roi", roi)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    # cv2.imshow("New", region_of_interest_image)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()