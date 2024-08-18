from cococar_lib.utils import PIDController
from cococar_lib import CocoCar
import time

car = CocoCar()
pid = PIDController(0.000375, 0, 0)
position_setpoint = 640


def x_midpoint(a, b):
    return (a[0] + b[0]) / 2


while True:
    markers = car.camera.detect_aruco_markers()

    if len(markers) == 0:
        car.drive.set_speed(0, 0)
        print(pid.get_output(0))  # so that derivative is also updating
    else:
        corners = markers[0]['corners']
        col_position = x_midpoint(corners[0], corners[1])
        position_error = -(col_position - position_setpoint)
        output = pid.get_output(position_error)
        print(output)
        car.drive.drive(0, output)

    time.sleep(0.1)
