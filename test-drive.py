from cococar_lib import CocoCar
import time

car = CocoCar()

TURN_FACTOR = 0.6

while True:
    x = car.controller.get_channel(car.controller.RIGHT_X) * TURN_FACTOR
    y = car.controller.get_channel(car.controller.RIGHT_Y)

    left = x + y
    right = x - y

    print(f'x: {x:.3f}, y: {y:.3f}, left: {left:.3f}, right: {right:.3f}')

    car.set_drive(x, y)

    time.sleep(0.05)
