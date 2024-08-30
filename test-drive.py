from cococar_lib import CocoCar

car = CocoCar()

TURN_FACTOR = 0.6

average_x = []
average_y = []
DATA_POINTS_X = 6
DATA_POINTS_Y = 12


def update():
    global average_x, average_y

    x = car.controller.get_channel(car.controller.RIGHT_X) * TURN_FACTOR
    y = car.controller.get_channel(car.controller.RIGHT_Y)

    average_x.append(x)
    average_y.append(y)
    if len(average_x) > DATA_POINTS_X:
        average_x = average_x[-DATA_POINTS_X:]
    if len(average_y) > DATA_POINTS_Y:
        average_y = average_y[-DATA_POINTS_Y:]

    average_x_values = sum(average_x) / len(average_x)
    average_y_values = sum(average_y) / len(average_y)

    # print(f'x: {x:.3f}, y: {y:.3f}')

    car.set_drive(average_y_values, average_x_values)


car.set_update_callback(update)
