import cv2
import numpy as np
from object_detection import ObjectDetection
import math

# Initialize Object Detection
obj_detection = ObjectDetection()

cap = cv2.VideoCapture("Temp.mp4")

# Initialize count
count = 0
prev_frame_centre_points_list = []

tracking_objects = {}
track_id = 0

while True:
    ret, frame = cap.read()
    count += 1
    if not ret:
        break

    # Point current frame
    cur_frame_centre_points_list = []

    # Detect objects on frame
    (class_ids, scores, boxes) = obj_detection.detect(frame)
    for box in boxes:
        (x, y, w, h) = box
        center_x = int((x + x + w) / 2)
        center_y = int((y + y + h) / 2)
        cur_frame_centre_points_list.append((center_x, center_y))
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Only at the beginning we compare previous and current frame
    if count <= 2:
        for current_point in cur_frame_centre_points_list:
            for previous_point in prev_frame_centre_points_list:
                distance = math.hypot(previous_point[0] - current_point[0], previous_point[1] - current_point[1])

                if distance < 20:
                    tracking_objects[track_id] = current_point
                    track_id += 1
    else:

        tracking_objects_copy = tracking_objects.copy()
        center_points_cur_frame_copy = cur_frame_centre_points_list.copy()

        for object_id, previous_point in tracking_objects_copy.items():
            object_exists = False
            for current_point in center_points_cur_frame_copy:
                distance = math.hypot(previous_point[0] - current_point[0], previous_point[1] - current_point[1])

                # Update IDs position
                if distance < 20:
                    tracking_objects[object_id] = current_point
                    object_exists = True
                    if current_point in cur_frame_centre_points_list:
                        cur_frame_centre_points_list.remove(current_point)
                    continue

            # Remove IDs lost
            if not object_exists:
                tracking_objects.pop(object_id)

        # Add new IDs found
        for current_point in cur_frame_centre_points_list:
            tracking_objects[track_id] = current_point
            track_id += 1

    for object_id, current_point in tracking_objects.items():
        cv2.circle(frame, current_point, 5, (0, 0, 255), -1)
        cv2.putText(frame, str(object_id), (current_point[0], current_point[1] - 7), 0, 1, (0, 0, 255), 2)

    print("Tracking objects")
    print(tracking_objects)

    print("CUR FRAME LEFT PTS")
    print(cur_frame_centre_points_list)

    cv2.imshow("Frame", frame)

    # Make a copy of the points
    prev_frame_centre_points_list = cur_frame_centre_points_list.copy()

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
