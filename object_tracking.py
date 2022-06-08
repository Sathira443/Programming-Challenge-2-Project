import cv2
import numpy as np
from sqlalchemy import false
from DangerArea import DangerArea
from collision_detection import detectCollision
from object_detection import ObjectDetection
import math

# defining danger area from the inputs of user.
print("\n  (x1,y1)   ____________  (x2,y1) \n           " +
    "/            \\ \n  (x0,y0) /              \\ (x2,y0) \n"+
    "         |                | \n         |                |   \n"+
    "  (x0,0) ------------------ (x3,0) \n")
# x0 =int(input("Enter x0 cordinate"))
# x1 =int(input("Enter x1 cordinate"))
# x2 =int(input("Enter x2 cordinate"))
# x3 =int(input("Enter x3 cordinate"))
# y0 =int(input("Enter y0 cordinate"))
# y1 =int(input("Enter y1 cordinate"))
# dangerArea = DangerArea(x0,x1,x2,x3,y0,y1)
dangerArea = DangerArea(10,450,1500,1900,800,500)

# Initialize Object Detection
obj_detection = ObjectDetection()

cap = cv2.VideoCapture("Temp3.m4v")
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)
# Initialize count
count = 0
# Store all the centre points of vehicles from the previous frame
previous_frame_object_list = []

tracking_objects = {}
track_id = 0

# Polygon corner points coordinates
pts = np.array([[10, 1000], [10, 800], [450, 600], [1500, 600], [1900, 800], [1900, 1000]], np.int32)

while True:
    ret, frame = cap.read()
    frame_copy = frame.copy()
    count += 1

    # If there are no more frames, break the loop
    if not ret:
        break

    # Trapezium
    cv2.polylines(frame, [pts], True, (0, 0, 255), 2)

    # roi = frame[500: 800, 10: 1900]
    # mask = object_detector.apply(roi)

    # Store all the centre points of vehicles from the current frame
    current_frame_Object_list = []

    # Detect objects on frame
    (class_ids, scores, boxes) = obj_detection.detect(frame)
    for box in boxes:
        (x, y, w, h) = box
        center_x = int((x + x + w) / 2)
        center_y = int((y + y + h) / 2)
        Variance_x = int(w/2)
        variance_y = int(h/2)
        current_frame_Object_list.append((center_x, center_y,Variance_x,variance_y))
        # Surround vehicle by a green box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Only at the beginning we compare previous and current frame
    if count <= 2:
        predicted_collisions = []
        for current_point in current_frame_Object_list:
            for previous_point in previous_frame_object_list:
                distance = math.hypot(previous_point[0] - current_point[0], previous_point[1] - current_point[1])

                if distance < 20:
                    isCollide = detectCollision(dangerArea,(current_point[0],current_point[1]),(previous_point[0],previous_point[1]),fps)
                    if isCollide != "no danger" :
                        predicted_collisions.append(isCollide)
                    tracking_objects[track_id] = current_point
                    track_id += 1
        
        if len(predicted_collisions) != 0:
            print("predicted collision :",predicted_collisions)
            
            # put the code for display the danger
            cv2.rectangle(frame_copy, (0, 0), (1920, 1080), (0, 0, 155),-1)
            
            alpha = 0.1  # Transparency factor.
            frame = cv2.addWeighted(frame_copy, alpha, frame, 0.8, 0)
            warning = ''
            for item in predicted_collisions:
                warning+= item[0] + '\t'
            cv2.putText(frame,warning , (640,360), 0, 1, (0, 0, 255), 2)
            ############ ends here add text danger
        
        print (current_frame_Object_list,previous_frame_object_list)
    else:

        tracking_objects_copy = tracking_objects.copy()
        center_points_cur_frame_copy = current_frame_Object_list.copy()

        predicted_collisions = []  # [X,Y,Z]
        for object_id, previous_point in tracking_objects_copy.items(): #(1,a) -> (1,b) -> (1,c)
            object_exists = False
            for current_point in center_points_cur_frame_copy:
                distance = math.hypot(previous_point[0] - current_point[0], previous_point[1] - current_point[1])

                # Update IDs position
                if distance < 20:
                    isCollide = detectCollision(dangerArea,(current_point[0],current_point[1]),(previous_point[0],previous_point[1]),fps)
                    
                    if isCollide != "no danger":
                        predicted_collisions.append(isCollide)
                    tracking_objects[object_id] = current_point
                    object_exists = True
                    if current_point in current_frame_Object_list:
                        current_frame_Object_list.remove(current_point)
                    continue
                    
            # Remove IDs lost
            if not object_exists:
                tracking_objects.pop(object_id)

        if len(predicted_collisions) != 0:
            
            print("predicted collision :",predicted_collisions)
            
            # put the code for display the danger            
            cv2.rectangle(frame_copy, (0, 0), (1920, 1080), (0, 0, 155),-1)
            
            alpha = 0.1  # Transparency factor.
            frame = cv2.addWeighted(frame_copy, alpha, frame, 0.9, 0)
            warning = ''
            for item in predicted_collisions:
                warning+= item[0] + '\t'
            cv2.putText(frame,warning , (640,360), 0, 1, (0, 0, 255), 2)
            ############ ends here add text danger
        
        # Add new IDs found
        for current_point in current_frame_Object_list:
            tracking_objects[track_id] = current_point
            track_id += 1

    for object_id, current_point in tracking_objects.items():
        cv2.circle(frame, (current_point[0],current_point[1]), 5, (0, 0, 255), -1)
        cv2.putText(frame, str(object_id), (current_point[0], current_point[1] - 7), 0, 1, (0, 0, 255), 2)
        
    print("Tracking objects")
    print(tracking_objects)

    print("CUR FRAME LEFT PTS")
    print(current_frame_Object_list)

    # This will show the frame in a new window
    cv2.imshow("Frame", frame)

    # Make a copy of the points
    previous_frame_object_list = current_frame_Object_list.copy()

    # Don't need to press any key to go through frame by frame
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
