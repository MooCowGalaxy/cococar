from cococar_lib.utils import PIDController
from cococar_lib import CocoCar
import time

car = CocoCar()
pid = PIDController(0.1, 0, 0)


def x_midpoint(a, b):
    return (a[1] + b[1]) / 2


while True:
    markers = car.camera.detect_aruco_markers()

    if len(markers) == 0:
        car.drive.set_speed(0, 0)
    else:
        corners = markers[0]['corners']
        col_position = x_midpoint(corners[0], corners[1])
        print(corners)

    time.sleep(0.05)
