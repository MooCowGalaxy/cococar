class RollingAverage:
    def __init__(self, max_length):
        self._max_length = max_length
        self._points = []

    def get_average(self):
        return sum(self._points) / len(self._points)

    def add_point(self, point):
        self._points.append(point)
        if len(self._points) > self._max_length:
            self._points.pop(0)
