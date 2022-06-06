import cv2
import numpy as np
from object_detection import ObjectDetection
import math

# Initialize Object Detection
obj_detection = ObjectDetection()

cap = cv2.VideoCapture("Temp3.m4v")

# Initialize count
count = 0
# Store all the centre points of vehicles from the previous frame
previous_frame_centre_point_list = []

tracking_objects = {}
track_id = 0

# Polygon corner points coordinates
pts = np.array([[10, 1000], [10, 800], [450, 500], [1500, 500], [1900, 800], [1900, 1000]], np.int32)

while True:
    ret, frame = cap.read()
    count += 1

    # If there are no more frames, break the loop
    if not ret:
        break

    #
    cv2.polylines(frame, [pts], True, (0, 0, 255), 2)

    # Store all the centre points of vehicles from the current frame
    current_frame_centre_point_list = []

    # Detect objects on frame
    (class_ids, scores, boxes) = obj_detection.detect(frame)
    for box in boxes:
        (x, y, w, h) = box
        center_x = int((x + x + w) / 2)
        center_y = int((y + y + h) / 2)
        current_frame_centre_point_list.append((center_x, center_y))
        # Surround vehicle by a green box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Only at the beginning we compare previous and current frame
    if count <= 2:
        for current_point in current_frame_centre_point_list:
            for previous_point in previous_frame_centre_point_list:
                distance = math.hypot(previous_point[0] - current_point[0], previous_point[1] - current_point[1])

                if distance < 20:
                    tracking_objects[track_id] = current_point
                    track_id += 1
    else:

        tracking_objects_copy = tracking_objects.copy()
        center_points_cur_frame_copy = current_frame_centre_point_list.copy()

        for object_id, previous_point in tracking_objects_copy.items():
            object_exists = False
            for current_point in center_points_cur_frame_copy:
                distance = math.hypot(previous_point[0] - current_point[0], previous_point[1] - current_point[1])

                # Update IDs position
                if distance < 20:
                    tracking_objects[object_id] = current_point
                    object_exists = True
                    if current_point in current_frame_centre_point_list:
                        current_frame_centre_point_list.remove(current_point)
                    continue

            # Remove IDs lost
            if not object_exists:
                tracking_objects.pop(object_id)

        # Add new IDs found
        for current_point in current_frame_centre_point_list:
            tracking_objects[track_id] = current_point
            track_id += 1

    for object_id, current_point in tracking_objects.items():
        cv2.circle(frame, current_point, 5, (0, 0, 255), -1)
        cv2.putText(frame, str(object_id), (current_point[0], current_point[1] - 7), 0, 1, (0, 0, 255), 2)

    print("Tracking objects")
    print(tracking_objects)

    print("CUR FRAME LEFT PTS")
    print(current_frame_centre_point_list)

    # This will show the frame in a new window
    cv2.imshow("Frame", frame)

    # Make a copy of the points
    previous_frame_centre_point_list = current_frame_centre_point_list.copy()

    # Don't need to press any key to go through frame by frame
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
