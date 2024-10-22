import socketio


class DataClient:
    def __init__(self):
        self.sio = socketio.SimpleClient()

    def connect(self):
        self.sio.connect('http://localhost:5555')
        print(f'Connected to data server!')

    def publish_data(self, topic: str, data: float):
        self.sio.emit('new_data', {'t': topic, 'd': data})

    def publish_lidar(self, lidar):
        """
        IMU data should be raw data from the LIDAR, with the beginning of the array representing 0 degrees and the end representing 360 degrees.
        It is recommended to only publish data up to 10 times/sec, as any more may cause lag.
        """
        self.sio.emit('new_lidar', lidar)
