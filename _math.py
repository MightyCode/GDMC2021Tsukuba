import math

def rotatePointAround(origin, point, angle) :
    return [  
        round(math.cos(angle) * (point[0] - origin[0]) - math.sin(angle) * (point[1] - origin[1]) + origin[0], 4),
        round(math.sin(angle) * (point[0] - origin[0]) + math.cos(angle) * (point[1] - origin[1]) + origin[1], 4),
    ]