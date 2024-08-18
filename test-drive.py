from cococar_lib import CocoCar
import time

car = CocoCar()

while True:
    x = car.controller.get_channel(car.controller.RIGHT_X)
    y = car.controller.get_channel(car.controller.RIGHT_Y)

    print(x, y)
    time.sleep(0.05)
