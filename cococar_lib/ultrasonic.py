from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory


class UltrasonicSensor:
    def __init__(self, echo_pin, trigger_pin):
        pin_factory = PiGPIOFactory()

        self._sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, pin_factory=pin_factory)

    def get_distance(self):
        """
        Returns the distance detected by the sensor in centimeters
        :return: Distance (cm)
        """
        return self._sensor.distance * 100
