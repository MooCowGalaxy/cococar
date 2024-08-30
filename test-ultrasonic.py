from cococar_lib import CocoCar
from cococar_lib.utils import remap_range, RollingAverage

car = CocoCar()

speed_average = RollingAverage(10)

MAX_SPEED = 0.2
STOPPING_DISTANCE = 50  # cm


def update():
    distance = car.ultrasonic.get_distance()

    speed = 0
    if distance > STOPPING_DISTANCE:
        speed = remap_range(distance, STOPPING_DISTANCE, 100, 0, MAX_SPEED)

    speed_average.add_point(speed)
    average = speed_average.get_average()

    car.set_drive(average, 0)


car.set_update_callback(update)
