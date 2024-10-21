# CocoBus
This repository contains the code used to power CocoBus - an autonomous cart that can carry dogs home.

## Project Structure
`cococar_lib` contains the main library used to control CocoBus. It includes utilities and helper functions to make it easier to develop code, such as PID controllers and interfaces to directly control the subsystems (such as motor movement or the camera).

`drive_server.py` is a Flask SocketIO server that sends PWM signals to the motors that control movement. This is used instead of simply sending signals in the user program because if the user program crashes, the most recent motor speeds would persist even though the program terminated. The drive server acts as a failsafe to automatically stop the motors if the user program lags or crashes, preventing the robot from veering off track and crashing.

`follower.py` is the main code used to follow an ArUco marker. It controls a camera mounted on a servo to track the marker, and controls the drivetrain to follow the marker using a PID controller.

## Miscellaneous Files
`animations` contains the source code for manim animations used in the video. It is not used to control the bot.

`test` contains testing scripts that were used to aid development, such as displaying a live feed of ArUco marker detection.

`test-drive.py` and `test-ultrasonic.py` are both test programs used to test functionality of the library and components. (The ultrasonic sensor has been removed from the design, as its range was too small for this use case)