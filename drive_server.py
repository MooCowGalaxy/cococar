from typing import Union

from flask import Flask
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler

import datetime
import pigpio
from cococar_lib.cococar import MOTOR_PINS, MIN_US, MAX_US, DEFAULT_MAX_SPEED
from cococar_lib.raw_drive import RawDrive

LEFT_PIN = MOTOR_PINS[0]
RIGHT_PIN = MOTOR_PINS[1]

app = Flask(__name__)
scheduler = APScheduler()
socketio = SocketIO(app, cors_allowed_origins="*")
pi = pigpio.pi()
drive = RawDrive(pi, LEFT_PIN, RIGHT_PIN, MIN_US, MAX_US, DEFAULT_MAX_SPEED)

last_drive_command: Union[datetime.datetime, None] = None


@socketio.on('drive')
def on_drive_command(data):
    global last_drive_command

    if 'left' not in data or 'right' not in data:
        return

    left_speed = data['left']
    right_speed = data['right']

    drive.set_speed(left_speed, right_speed)
    last_drive_command = datetime.datetime.now()


def listen():
    socketio.run(app, host='0.0.0.0', port=5050, use_reloader=False, debug=False, log_output=False)
    print('Drive server listening on localhost:5050!')


def scheduled_stop():
    if last_drive_command is None:
        return

    if (datetime.datetime.now() - last_drive_command) > datetime.timedelta(seconds=1):
        drive.set_speed(0, 0)
        print(f'Emergency stop activated at {datetime.datetime.now()}')


scheduler.add_job(id='Emergency Shut-Off', func=scheduled_stop, trigger="interval", seconds=1)

if __name__ == '__main__':
    scheduler.start()
    listen()
