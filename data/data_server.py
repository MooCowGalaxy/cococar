from flask import Flask, send_from_directory, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
import time


class DataServer:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/assets/<path:path>')
        def send_asset(path):
            return send_from_directory('assets', path)

        @self.socketio.on('new_data')
        def new_data(data):
            self.socketio.emit('data', {'t': data['t'], 'd': data['d'], 'x': round(time.time() * 1000)})

        @self.socketio.on('new_lidar')
        def new_lidar_data(data):
            self.socketio.emit('lidar', data)

        @self.socketio.on('new_lidar_lines')
        def new_lidar_line_data(data):
            self.socketio.emit('lidar_lines', {'data': data, 'time': round(time.time() * 1000)})

    def listen(self):
        self.socketio.run(self.app, host='0.0.0.0', port=5555, use_reloader=False, debug=False, log_output=False)
        print('init')


if __name__ == '__main__':
    DataServer().listen()
