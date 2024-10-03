from .camera import Camera
from .controller import Controller
from .drive_client import DriveClient
from .encoder import QuadratureEncoder
from .ultrasonic import UltrasonicSensor
from .utils import clamp
from enum import Enum
import pigpio
import time

CONTROLLER_INPUT_PINS = [11, 5, 6, 16, 8, 7]
MOTOR_PINS = [26, 19]  # left, right
ENCODER_PINS = [
    [15, 14],  # left pins
    [24, 23]   # right pins
]
ULTRASONIC_PINS = [27, 17]

MIN_US = 1050
MAX_US = 1950

LEFT_OFFSET = 0
RIGHT_OFFSET = 0
DEFAULT_TURN_FACTOR = 0.5
DEFAULT_MAX_SPEED = 1


class CarState(Enum):
    STOPPED = 0
    MANUAL = 1
    AUTO = 2


class CocoCar:
    def __init__(self, turn_factor=DEFAULT_TURN_FACTOR, max_speed=DEFAULT_MAX_SPEED):
        self.pi = pigpio.pi()
        # self.left_encoder = QuadratureEncoder(self.pi, pin_A=ENCODER_PINS[0][0], pin_B=ENCODER_PINS[0][1])
        # self.right_encoder = QuadratureEncoder(self.pi, pin_A=ENCODER_PINS[1][0], pin_B=ENCODER_PINS[1][1])
        self.controller = Controller(self.pi, CONTROLLER_INPUT_PINS, MIN_US, MAX_US)
        self.ultrasonic = UltrasonicSensor(ULTRASONIC_PINS[0], ULTRASONIC_PINS[1])

        print(f'Connecting to drive server...')
        self._drive = DriveClient(max_speed)
        self._drive.connect()
        self._drive.set_speed(0, 0)
        print(f'--------------------------------------------------------')

        self.camera = Camera()
        self.state = CarState.STOPPED
        self.turn_factor = turn_factor
        self.max_speed = max_speed
        self._update_callback = None

    def set_update_callback(self, update_callback, delay=0.05):
        self._update_callback = update_callback

        while True:
            state = round(self.controller.get_channel(5) * 2)
            if state != self.state.value:
                if state == CarState.STOPPED.value:
                    self.state = CarState.STOPPED
                    self._drive.set_speed(0, 0)
                elif state == CarState.MANUAL.value:
                    self.state = CarState.MANUAL
                elif state == CarState.AUTO.value:
                    self.state = CarState.AUTO
                print(f'Switched state to {self.state.name}')

            if self._update_callback is not None:
                self._update_callback()

            if self.state == CarState.MANUAL:
                x = self.controller.get_channel(self.controller.RIGHT_X) * self.turn_factor
                y = self.controller.get_channel(self.controller.RIGHT_Y) * self.max_speed

                left = x + y
                right = x - y

                self._drive.set_speed(left, right)

            time.sleep(delay)

    def set_drive(self, speed, turn, max_speed=None):
        if self.state != CarState.AUTO:
            return

        if max_speed is None:
            max_speed = self.max_speed

        # speed = -speed
        left = clamp(float(turn + speed), -max_speed, max_speed)
        right = clamp(float(turn - speed), -max_speed, max_speed)
        self._drive.set_speed(left, right)
