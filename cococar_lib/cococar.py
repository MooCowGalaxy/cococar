from .encoder import QuadratureEncoder
from .controller import Controller
from .drive import Drive
from .camera import Camera
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

MIN_US = 1050
MAX_US = 1950

LEFT_OFFSET = 0
RIGHT_OFFSET = 0


class CarState(Enum):
    STOPPED = 0
    MANUAL = 1
    AUTO = 2


class CocoCar:
    def __init__(self):
        self.pi = pigpio.pi()
        self.left_encoder = QuadratureEncoder(self.pi, pin_A=ENCODER_PINS[0][0], pin_B=ENCODER_PINS[0][1])
        self.right_encoder = QuadratureEncoder(self.pi, pin_A=ENCODER_PINS[1][0], pin_B=ENCODER_PINS[1][1])
        self.controller = Controller(self.pi, CONTROLLER_INPUT_PINS, MIN_US, MAX_US)
        self.drive = Drive(self.pi, MOTOR_PINS[0], MOTOR_PINS[1], MIN_US, MAX_US, LEFT_OFFSET, RIGHT_OFFSET)
        self.camera = Camera()
        self.state = CarState.STOPPED
        self.update_callback = None

    def set_update_callback(self, update_callback, delay=0.05):
        self.update_callback = update_callback

        while True:
            state = round(self.controller.get_channel(5))
            if state != self.state.value:
                if state == CarState.STOPPED.value:
                    self.state = CarState.STOPPED
                elif state == CarState.MANUAL.value:
                    self.state = CarState.MANUAL
                elif state == CarState.AUTO.value:
                    self.state = CarState.AUTO
                print(f'Switched state to {self.state.name}')

            if self.update_callback is not None:
                self.update_callback()

            time.sleep(delay)

    def set_drive(self, speed, angle, max_speed=1):
        if self.state != CarState.AUTO:
            return

        speed = -speed
        left = clamp(angle + speed, -max_speed, max_speed)
        right = clamp(angle - speed, -max_speed, max_speed)
        self.drive.set_speed(left, right)
