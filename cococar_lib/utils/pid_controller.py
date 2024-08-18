class PIDController:
    def __init__(self, kP=0, kI=0, kD=0):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self._history = []

    def _derivative(self, current_error):
        # prevent out of bounds error
        if len(self._history) < 5:
            return 0

        numerator = -current_error + 8 * self._history[0] - 8 * self._history[2] + self._history[3]

        return numerator / 12

    def get_output(self, error):
        output = self.kP * error + self.kI * sum(self._history) + self.kD * self._derivative(error)

        self._history.insert(0, error)
        # keep 10 data points
        if len(self._history) > 10:
            self._history = self._history[:10]

        return output
