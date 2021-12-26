from enum import *

class AxisEnums(Enum):
    X = 0
    Y = 1
    Z = 2
class FacingEnums(Enum):
    Xp = 0
    Xn = 1
    Yp = 2
    Yn = 3
    Zp = 4
    Zn = 5

class Orientation:
    def __init__(self):
        self.Facing = FacingEnums.Xp
        self.Rotation = 0

    def setFacing(self, fac : FacingEnums):
        self.Facing = fac

    def setRotation(self, rot : int):
        if rot <0 or rot > 3:
            None
        else:
            self.Rotation = rot

    def get_rotation_factors(self, dest_ori: Orientation):
        if self.Facing == dest_ori.Facing:



class Scanner:
    def __init__(self, ori : Orientation):
        self.Orient = ori
        self.Beacons = []

    def add_beacon(self, beac : tuple):
        self.Beacons.append(beac)

    def rotate(self, axis : AxisEnums, clic: int):
        if axis == AxisEnums.X:
            for i in range(clic):
                for idx, b in enumerate(self.Beacons):
                    out_b = (b[AxisEnums.X], -b[AxisEnums.Z], b[AxisEnums.Y])
                    self.Beacons[idx] = out_b
        elif axis == AxisEnums.Y:
            for i in range(clic):
                for idx, b in enumerate(self.Beacons):
                    out_b = (b[AxisEnums.Z], b[AxisEnums.Y], -b[AxisEnums.X])
                    self.Beacons[idx] = out_b
        elif axis == AxisEnums.Z:
            for i in range(clic):
                for idx, b in enumerate(self.Beacons):
                    out_b = (b[AxisEnums.Y], -b[AxisEnums.X], b[AxisEnums.Z])
                    self.Beacons[idx] = out_b

o1 = Orientation(0)

day18_ori_example = [
    (-1,-1,1),
    (-2,-2,2),
    (-3,-3,3),
    (-2,-3,1),
    (5,6,-4),
    (8,0,7),
    ]
day18_ori_example2 = [
    (1, -1, 1),
    (2, -2, 2),
    (3, -3, 3),
    (2, -1, 3),
    (-5, 4, -6),
    (-8, -7, 0),
    ]
scan1 = Scanner(o1)
for b in day18_ori_example:
    scan1.add_beacon(b)
scan1_norm_beacons = scan1.get_rotated_beacons()
print(scan1_norm_beacons)
for i in range(1,24):
    my_o = Orientation(i)
    scan2 = Scanner(my_o)
    for b in day18_ori_example2:
        scan2.add_beacon(b)
    scan2_norm_beacons = scan2.get_normalized_beacons()
    print(scan2_norm_beacons)
    if scan1_norm_beacons == scan2_norm_beacons:
        print(f"Found orientation {i} to produce same list")
