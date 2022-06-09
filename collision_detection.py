import sys
from turtle import distance
from numpy import empty
from sympy import *
from DangerArea import DangerArea

#get the exact point of intersecting and intersect with on which function.
def FindIntersectionPoints(inter_f, current_point):
    
    #get all intersections from 5 different functions.
    intersection_points = []
    for n in range(len(inter_f)):
        if len(inter_f[n]) != 0:
            if type(inter_f[n]) == Segment2D:
                p1 = inter_f[n].p1
                p2 = inter_f[n].p2
                d1 = p1.distance(current_point)
                d2 = p2.distance(current_point)
                if d1 < d2:
                    intersection_points.append((p1,n))
                else:
                    intersection_points.append((p2,n))
            else:
                intersection_points.append((inter_f[n],n))
    
    #find the minimum distance point from all intersecting points.
    distance = sys.maxsize
    minInterPoint = ()
    for inter_point in intersection_points:
        distanceToP = inter_point[0][0].distance(current_point)
        if distanceToP < distance:
            distance = distanceToP
            minInterPoint = inter_point                                             #([Point(1,0)],0)
    
    return minInterPoint


# MAIN FUNCTION
# 
# 
# 
# 
#function for cheching if object is collide or not.
def detectCollision(dangerArea,curr_point,pre_point,fps):
    current_point = Point(curr_point)
    previous_point = Point(pre_point)
    if current_point.equals(previous_point): #assumption
        return "no danger"
    
    # print(current_point,previous_point,curr_point,pre_point)
    inter_f = []
    movement_line = Line(current_point,previous_point)
    
    #get intersecting points with functions.
    inter_f.append(movement_line.intersection(dangerArea.f0))
    inter_f.append(movement_line.intersection(dangerArea.f1))
    inter_f.append(movement_line.intersection(dangerArea.f2))
    inter_f.append(movement_line.intersection(dangerArea.f3))
    inter_f.append(movement_line.intersection(dangerArea.f4))

    #if no intersections return no danger.
    if len(inter_f[0]) == 0 and len(inter_f[1]) == 0 and len(inter_f[2]) == 0 and len(inter_f[3]) == 0 and len(inter_f[4]) == 0:
        return "no danger"
    
    #else return the direction of danger.
    else:
        timeperiod = 1/fps
        collision_point = FindIntersectionPoints(inter_f,current_point)                 #([Point(1,0)],0)
        velocity  = current_point.distance(previous_point)/timeperiod
        T=current_point.distance(collision_point[0][0])/velocity  #approximated Time for collision is T
        
        if T < 2:
            if collision_point[1] == 0:
                return ("danger on your left")
                #return ("danger on your left",collision_point,current_point,previous_point,timeperiod,velocity,T)
            if collision_point[1] == 1:
                return ("danger on your left")
                #return ("danger on your left",collision_point,current_point,previous_point,timeperiod,velocity,T)
            if collision_point[1] == 2:
                return ("danger on your front")
                #return ("danger on your front",collision_point,current_point,previous_point,timeperiod,velocity,T)
            if collision_point[1] == 3:
                return ("danger on your right")
                #return ("danger on your right",collision_point,current_point,previous_point,timeperiod,velocity,T)
            if collision_point[1] == 4:
                return ("danger on your right")
                #return ("danger on your right",collision_point,current_point,previous_point,timeperiod,velocity,T)
        else:
            return "no danger"

# dangerArea = DangerArea(0,1,2,3,0,1)
# detectCollision(dangerArea,(0,1),(4,1))