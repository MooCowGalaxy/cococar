from cococar_lib.utils import PIDController, clamp
from cococar_lib import CocoCar

car = CocoCar()
speed_pid = PIDController(0.0004, 0, 0.001)
angle_pid = PIDController(0.0004, 0, 0.0002)
max_output = 0.8
position_setpoint = 320
distance_setpoint = 70


def x_midpoint(a, b):
    return (a[0] + b[0]) / 2


speed = 0
angle = 0
no_detection_count = 0


def update():
    global speed, angle, no_detection_count

    markers = car.camera.detect_aruco_markers()

    if len(markers) == 0:
        if no_detection_count == 20:
            car.set_drive(0, 0)
            speed = 0
            angle = 0
        speed *= 0.95
        angle *= 0.95
        car.set_drive(-speed, angle, max_output)
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
        print(-speed, angle, markers[0]['distance'])
        car.set_drive(-speed, angle, max_output)


car.set_update_callback(update)
