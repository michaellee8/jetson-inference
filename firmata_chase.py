from pymata4 import pymata4
from time import sleep
import jetson.inference
import jetson.utils

import argparse
import sys
from os import path

SERVO_PAN_PIN = 48
SERVO_TILT_PIN = 47

LEFT_SONIC_ECHO = 64 # A10 PK2
LEFT_SONIC_TRIG = 65 # A11 PK3

RIGHT_SONIC_ECHO = 60 # A6 PF6
LEFT_SONIC_TRIG = 61 # A7 PF7

# A B
# C D
#  |
#  V

FORWARD_VEC = [1, 1,
               1, 1]

BACKWARD_VEC = [-1, -1,
                -1, -1]

ROTATE_CLOCKWISE_VEC = [-1, 1,
                        -1, 1]

ROTATE_ANTICLOCKWISE_VEC = [1, -1,
                            1, -1]

LEFT_VEC = [-1, 1,
            1, -1]

RIGHT_VEC = [1, -1,
             -1, 1]


STOP_VEC = [0, 0,
            0, 0]

MOTOR_NAMES = ["A", "B", "C", "D"]
PWM_PINS = [12, 8, 9, 5]
DIRA_PINS = [34, 37, 43, 26]
DIRB_PINS = [35, 36, 42, 27]

board = pymata4.Pymata4()


# print(board.get_firmata_version())

NORMAL_PWM = 100

FORWARD_COEFFICIENT = 1
ROTATE_COEFFICIENT = 1
SIDE_COEFFICIENT = 0.1

board.set_pin_mode_servo(SERVO_PAN_PIN)

angle = 45
while angle <= 135:
    board.servo_write(SERVO_PAN_PIN, angle)
    angle += 1
    sleep(0.1)


board.shutdown()