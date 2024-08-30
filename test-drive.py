from cococar_lib import CocoCar
from cococar_lib.utils import RollingAverage

car = CocoCar()

TURN_FACTOR = 0.6

average_x = RollingAverage(6)
average_y = RollingAverage(12)


def update():
    global average_x, average_y

    x = car.controller.get_channel(car.controller.RIGHT_X) * TURN_FACTOR
    y = car.controller.get_channel(car.controller.RIGHT_Y)

    average_x.add_point(x)
    average_y.add_point(y)

    average_x_values = average_x.get_average()
    average_y_values = average_y.get_average()

    # print(f'x: {x:.3f}, y: {y:.3f}')

    car.set_drive(average_y_values, average_x_values)


car.set_update_callback(update)
