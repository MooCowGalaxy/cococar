from .encoder import QuadratureEncoder
from .controller import Controller
from .drive import Drive
import pigpio

CONTROLLER_INPUT_PINS = [11, 5, 6, 16, 20, 21]
MOTOR_PINS = [26, 19]  # left, right
ENCODER_PINS = [
    [15, 14],  # left pins
    [24, 23]   # right pins
]

MIN_US = 1020
MAX_US = 2030

LEFT_OFFSET = -40
RIGHT_OFFSET = 0


class CocoCar:
    def __init__(self):
        self.pi = pigpio.pi()
        self.left_encoder = QuadratureEncoder(self.pi, pin_A=ENCODER_PINS[0][0], pin_B=ENCODER_PINS[0][1])
        self.right_encoder = QuadratureEncoder(self.pi, pin_A=ENCODER_PINS[1][0], pin_B=ENCODER_PINS[1][1])
        self.controller = Controller(self.pi, CONTROLLER_INPUT_PINS, MIN_US, MAX_US)
        self.drive = Drive(self.pi, MOTOR_PINS[0], MOTOR_PINS[1], MIN_US, MAX_US, LEFT_OFFSET, RIGHT_OFFSET)
