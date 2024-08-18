from cococar_lib.utils import PIDController, clamp
from cococar_lib import CocoCar
import time

car = CocoCar()
speed_pid = PIDController(0.002, 0, 0.02)
angle_pid = PIDController(0.0006, 0, 0.0003)
max_output = 0.7
position_setpoint = 320
distance_setpoint = 40


def x_midpoint(a, b):
    return (a[0] + b[0]) / 2


speed = 0
angle = 0
no_detection_count = 0
while True:
    markers = car.camera.detect_aruco_markers()

    if len(markers) == 0:
        if no_detection_count == 10:
            car.drive.set_speed(0, 0)
            speed = 0
            angle = 0
        speed *= 0.9
        angle *= 0.9
        car.drive.drive(speed, angle, max_output)
        speed_pid.get_output(0)
        angle_pid.get_output(0)  # so that derivative is also updating
        no_detection_count += 1
    else:
        no_detection_count = 0

        corners = markers[0]['corners']
        col_position = x_midpoint(corners[0], corners[1])
        position_error = -(col_position - position_setpoint)

        distance_error = markers[0]['distance'] - distance_setpoint

        delta_speed = speed_pid.get_output(distance_error)
        print(delta_speed)
        speed += delta_speed
        speed = clamp(speed, -max_output, max_output)
        angle = clamp(angle_pid.get_output(position_error), -max_output, max_output)
        print(speed, angle, markers[0]['distance'])
        car.drive.drive(speed, angle, max_output)

    time.sleep(0.08)
