from cococar_lib import CocoCar

car = CocoCar()

TURN_FACTOR = 0.6


def update():
    x = car.controller.get_channel(car.controller.RIGHT_X) * TURN_FACTOR
    y = car.controller.get_channel(car.controller.RIGHT_Y)

    print(f'x: {x:.3f}, y: {y:.3f}')

    car.set_drive(y, x)


car.set_update_callback(update)
