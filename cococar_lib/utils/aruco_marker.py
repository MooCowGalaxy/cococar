import math


def line_length(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def get_marker_distance(points):
    side = line_length(points[0], points[1])

    distance = 1 / side
    return distance * 1500 / 2.54  # conversion factor to inches
