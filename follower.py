from cococar_lib.utils import PIDController, clamp, remap_range
from cococar_lib import CocoCar, Servo
import time

car = CocoCar()
servo_range = 270
servo = Servo(car.pi, 13, servo_range)
speed_pid = PIDController(0.0004, 0, 0.001)
angle_pid = PIDController(0.0004, 0, 0.0002)
max_output = 0.8
position_setpoint = 320
distance_setpoint = 70

camera_fov = 110
actual_servo_angle = 0
target_servo_angle = 0
servo_speed = 150  # degrees per second


def x_midpoint(a, b):
    return (a[0] + b[0]) / 2


speed = 0
angle = 0
no_detection_count = 0
previous_time = time.time()


def update():
    global speed, angle, no_detection_count, previous_time, target_servo_angle, actual_servo_angle
    dt = time.time() - previous_time
    previous_time = time.time()

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

        marker_angle = remap_range(col_position, 0, 1920, -camera_fov / 2, camera_fov / 2)
        target_servo_angle = actual_servo_angle + marker_angle
        servo.turn(target_servo_angle)

        camera_servo_offset = remap_range(actual_servo_angle, -camera_fov, camera_fov, 0, 1920, False)

        position_error = -(col_position + camera_servo_offset - position_setpoint)

        distance_error = markers[0]['distance'] - distance_setpoint

        delta_speed = speed_pid.get_output(distance_error)
        speed += delta_speed
        speed = clamp(speed, -max_output, max_output)
        angle = clamp(angle_pid.get_output(position_error), -max_output, max_output)
        car.set_drive(-speed, angle, max_output)

    # update actual servo position
    delta_servo_angle = clamp(actual_servo_angle - target_servo_angle, 0, servo_speed * dt)
    if target_servo_angle < actual_servo_angle:
        actual_servo_angle -= delta_servo_angle
    elif target_servo_angle > actual_servo_angle:
        actual_servo_angle += delta_servo_angle
    actual_servo_angle = clamp(actual_servo_angle, -servo_range, servo_range)


car.set_update_callback(update)
