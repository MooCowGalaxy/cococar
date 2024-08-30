import socketio
from .utils import clamp


class DriveClient:
    def __init__(self, max_speed=0.8):
        self.sio = socketio.SimpleClient()
        self._max_speed = max_speed

    def connect(self):
        self.sio.connect('http://localhost:5050')
        print(f'Connected to drive server!')

    def set_speed(self, left_speed, right_speed):
        left_clamped = clamp(left_speed, -self._max_speed, self._max_speed)
        right_clamped = clamp(right_speed, -self._max_speed, self._max_speed)

        self.sio.emit('drive', {
            'left': left_clamped,
            'right': right_clamped
        })
