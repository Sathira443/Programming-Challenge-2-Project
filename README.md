# Programming-Challenge-2-Project

We were asked to develop a Vehicle Collision Warning System for CS2212 - Programming 
Challenge II module. (CSE- 19 batch- UoM)

Our team consist of 4 members of 19 batch(CSE-UoM). 
● Shihan Vidulanka
● Sahan Caldera
● Harshani Bandara
● Sathira liyanapathirana


System requirements of the developed system include,
● Process a video feed from a car dash cam and follow the movement of vehicles in 
the video stream. We used a recorded video as input for this project. 
● Predict the movement of the tracked vehicles two seconds in advance. 
● Users should be able to designate an area as a danger zone 
● If a vehicle is expected to reach the danger zone within the next two seconds, a 
warning will be generated.

Python was used as the main programming language. Yolov4 object detection model, 
OpenCV, Numpy and Sympy libraries were used as well. YoloV4 and OpenCV were used for 
object detection and object tracking. NumPy is a Python library for manipulating arrays. 
SymPy is a Python library for symbolic mathematics which we used to do calculations with 
lines.

Nowadays, a considerable number of people have died from vehicle accidents which are 
about 42,338. Mainly Carelessness, Overspeeding, rash driving, exhaustion, and violation of 
rules affect the road accident from the driver's side. If we can provide a solution from the 
driver's side to avoid these mistakes, we will be able to reduce the percentage of vehicle 
accidents. As a solution to this problem, we have developed Vehicle Collision Warning 
System using OpenCV, and Yolo with python language. We can use the data of the cameras 
and the sensors to develop the system. 

Further Improvements
● For this specific project, we calculated the equation of the vehicle direction by only 
using two points of 2 different frames of the same vehicle. This is regarded as less 
accurate in real world scenarios. To be more accurate, we can get at least 10 frames 
and calculate an equation using 10 different points.
● Also, the minimum distance line between the danger line and the object was started 
from the midpoint of an object. But this distance may not be accurate because the 
lowest distance between the danger line and the object will be starting from the 
radiator.
● For more accurate collision detection, data of sensors with multiple cameras can be 
used as well.
● Technical errors were mainly given by the YOLO because when detecting the 
vehicles in a single frame, sometimes the centerpoints of the vehicle differ in larger 
amounts even if the object's position does not vary. So we cannot predict the 
accurate position of the vehicle by getting only the centre point. To reduce this 
failure, we can get corner points of detected objects and evaluate if the vehicle 
collided with those points in the danger area.
● On the other hand the methodology we use to calculate collision time is more simple 
and the error occurring due to centre points is very high. To reduce this, we can 
predict the collision time by getting centerpoints of more frames and predict better 
direction of the vehicle.
● For this project we assumed a distance of 2 pixels is equal to distance between two 
vehicles. But in a real world scenario, this might not be accurate. We may need to 
find the actual distance according to the relevant dashcam video steam and calculate 
the actual ratio between distance and pixels.


