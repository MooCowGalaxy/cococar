from cococar_lib.utils import PIDController, clamp
from cococar_lib import CocoCar
import time

car = CocoCar()
pid = PIDController(0.001, 0, 0)
max_output = 0.25
position_setpoint = 320


def x_midpoint(a, b):
    return (a[0] + b[0]) / 2


no_detection_count = 0
while True:
    markers = car.camera.detect_aruco_markers()

    if len(markers) == 0:
        if no_detection_count == 10:
            car.drive.set_speed(0, 0)
        print(pid.get_output(0))  # so that derivative is also updating
        no_detection_count += 1
    else:
        no_detection_count = 0
        corners = markers[0]['corners']
        col_position = x_midpoint(corners[0], corners[1])
        position_error = -(col_position - position_setpoint)
        output = clamp(pid.get_output(position_error), -max_output, max_output)
        print(output, markers[0]['distance'])
        car.drive.drive(0, output)

    time.sleep(0.1)
