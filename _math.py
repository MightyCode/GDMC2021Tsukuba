import math


def isPointInSquare(point, square):
    if (square[0] <= point[0] and square[3] >= point[0]):
        if (square[1] <= point[1] and square[4] >= point[1]):
            if (square[2] <= point[2] and square[5] >= point[2]):
                return True

    return False
    

def rotatePointAround(origin, point, angle) :
    return [  
        round(math.cos(angle) * (point[0] - origin[0]) - math.sin(angle) * (point[1] - origin[1]) + origin[0], 4),
        round(math.sin(angle) * (point[0] - origin[0]) + math.cos(angle) * (point[1] - origin[1]) + origin[1], 4),
    ]
      