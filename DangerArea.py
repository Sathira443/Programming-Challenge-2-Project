from tkinter import Y
from sympy import *

class DangerArea():
    def __init__(self,x0,x1,x2,x3,y0,y1):
        self.x0 = x0
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.y0 = y0
        self.y1 = y1
        
        self.f0 = Segment((x0,1000),(x0,y0))
        self.f1 = Segment((x0,y0),(x1,y1))
        self.f2 = Segment((x1,y1),(x2,y1))
        self.f3 = Segment((x2,y1),(x3,y0))
        self.f4 = Segment((x3,y0),(x3,1000))