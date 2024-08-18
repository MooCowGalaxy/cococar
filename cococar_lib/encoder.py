import pigpio


def _decode(A, B):
    return (A << 1) | B


class QuadratureEncoder:
    def __init__(self, pi, pin_A, pin_B, resolution=537.6):
        self._pi = pi
        self._pin_A = pin_A
        self._pin_B = pin_B
        self._resolution = resolution

        self._position = 0
        self._state = 0

        pi.set_mode(pin_A, pigpio.INPUT)
        pi.set_mode(pin_B, pigpio.INPUT)
        pi.set_pull_up_down(pin_A, pigpio.PUD_UP)
        pi.set_pull_up_down(pin_B, pigpio.PUD_UP)

        self._cb_A = pi.callback(pin_A, pigpio.EITHER_EDGE, self._update)
        self._cb_B = pi.callback(pin_B, pigpio.EITHER_EDGE, self._update)

    def _update(self, _channel, _level, _tick):
        A = self._pi.read(self._pin_A)
        B = self._pi.read(self._pin_B)

        new_state = _decode(A, B)

        if new_state != self._state:
            if (self._state == 0 and new_state == 1) or \
                    (self._state == 1 and new_state == 3) or \
                    (self._state == 3 and new_state == 2) or \
                    (self._state == 2 and new_state == 0):
                self._position += 1
            elif (self._state == 0 and new_state == 2) or \
                    (self._state == 2 and new_state == 3) or \
                    (self._state == 3 and new_state == 1) or \
                    (self._state == 1 and new_state == 0):
                self._position -= 1

            self._state = new_state

    def get_revolutions(self):
        return self._position / self._resolution

    def set_revolutions(self, revolutions):
        self._position = int(revolutions * self._resolution)

    def cancel(self):
        self._cb_A.cancel()
        self._cb_B.cancel()
