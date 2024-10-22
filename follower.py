from cococar_lib.utils import PIDController, clamp, remap_range
from cococar_lib import CocoCar, Servo
import time

car = CocoCar()
servo_range = 270
servo = Servo(car.pi, 13, servo_range)
# speed_pid = PIDController(0.0009, 0, 0.0011)
speed_pid = PIDController(0.01, 0, 0.005)
angle_servo_pid = PIDController(0.0003, 0, 0.0001)
angle_pid = PIDController(0.35, 0, 0.07)
max_output = 0.6
position_setpoint = 320
distance_setpoint = 60
stop_distance = 25

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
        # if no_detection_count == 20:
        if speed < 0.08:
            car.set_drive(0, 0)
            speed = 0
            angle = 0
            target_servo_angle = 0
            actual_servo_angle = 0
            servo.turn(0)
        speed *= 0.95
        angle *= 0.95
        if speed != 0: print(f'ArUco marker not detected, slowing speed to {speed}')
        car.set_drive(-speed if speed > 0 else 0, angle, max_output)
        speed_pid.get_output(0)
        angle_pid.get_output(0)  # so that derivative is also updating
        no_detection_count += 1
    else:
        no_detection_count = 0

        corners = markers[0]['corners']
        col_position = x_midpoint(corners[0], corners[1])

        marker_angle = remap_range(col_position, 0, 640, -camera_fov / 2, camera_fov / 2)
        marker_angle_error = -marker_angle
        servo_pid_output = angle_servo_pid.get_output(marker_angle_error)
        target_servo_angle += servo_pid_output
        target_servo_angle = clamp(target_servo_angle, -servo_range / 2, servo_range / 2)
        servo.turn(target_servo_angle)

        camera_servo_offset = remap_range(actual_servo_angle, -camera_fov, camera_fov, 0, 1920, False)

        position_error = -(col_position + camera_servo_offset - position_setpoint)

        distance_error = markers[0]['distance'] - distance_setpoint

        # delta_speed = speed_pid.get_output(distance_error)
        # if delta_speed < 0:
        #     delta_speed *= 1.65
        # speed += delta_speed
        speed = speed_pid.get_output(distance_error)
        speed = clamp(speed, -max_output, max_output)
        print(speed, distance_error)
        angle = -clamp(angle_pid.get_output(-target_servo_angle), -max_output, max_output)
        # print(target_servo_angle, angle)
        if markers[0]['distance'] <= stop_distance:
            car.set_drive(0, angle, max_output)
        else:
            car.set_drive(-speed if speed > 0 else 0, angle, max_output)

    # update actual servo position
    delta_servo_angle = clamp(abs(actual_servo_angle - target_servo_angle), 0, servo_speed * dt * 0.05)
    if target_servo_angle < actual_servo_angle:
        actual_servo_angle -= delta_servo_angle
    elif target_servo_angle > actual_servo_angle:
        actual_servo_angle += delta_servo_angle
    actual_servo_angle = clamp(actual_servo_angle, -servo_range / 2, servo_range / 2)


car.set_update_callback(update)
