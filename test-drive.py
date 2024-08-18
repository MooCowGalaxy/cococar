from cococar_lib import CocoCar
import time

car = CocoCar()

while True:
    x = car.controller.get_channel(car.controller.RIGHT_X)
    y = car.controller.get_channel(car.controller.RIGHT_Y)

    left = x + y
    right = x - y

    print(f'x: {x:.3f}, y: {y:.3f}, left: {left:.3f}, right: {right:.3f}')

    car.drive.set_speed(left, right)

    time.sleep(0.05)
