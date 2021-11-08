from typing import List
from pymata4 import pymata4
from time import sleep
from math import floor
import jetson.inference
import jetson.utils

import argparse
import sys
from os import path

SERVO_PAN_PIN = 48
SERVO_TILT_PIN = 47

LEFT_SONIC_ECHO_PIN = 64  # A10 PK2
LEFT_SONIC_TRIG_PIN = 65  # A11 PK3

RIGHT_SONIC_ECHO_PIN = 60  # A6 PF6
LEFT_SONIC_TRIG_PIN = 61  # A7 PF7

NORMAL_PWM = 100

FORWARD_COEFFICIENT = 1
ROTATE_COEFFICIENT = 1
SIDE_COEFFICIENT = 0.1

MAX_ANGLE = 135
MIN_ANGLE = 45

# A B
# C D
#  |
#  V

FORWARD_VEC = [-1, 1, -1, 1]

BACKWARD_VEC = [1, -1, 1, -1]

ROTATE_CLOCKWISE_VEC = [1, 1, 1, 1]

ROTATE_ANTICLOCKWISE_VEC = [-1, -1, -1, -1]

LEFT_VEC = [-1, -1, 1, 1]

RIGHT_VEC = [1, 1, -1, -1]


STOP_VEC = [0, 0,
            0, 0]

MOTOR_NAMES = ["A", "B", "C", "D"]
PWM_PINS = [12, 8, 9, 5]
DIRA_PINS = [34, 37, 43, 58]
DIRB_PINS = [35, 36, 42, 59]


def execute_movement_vector(board: pymata4.Pymata4, vec: List[float]):
    for motor_index in range(4):
        outn = int(floor(vec[motor_index] * NORMAL_PWM))
        if outn > 0:
            board.digital_write(DIRA_PINS[motor_index], 0)
            board.digital_write(DIRB_PINS[motor_index], 1)
        else:
            board.digital_write(DIRA_PINS[motor_index], 1)
            board.digital_write(DIRB_PINS[motor_index], 0)
        outn = int(abs(outn))
        board.pwm_write(PWM_PINS[motor_index], outn)
    return


def clamp_angle(angle: int) -> int:
    if angle < MIN_ANGLE:
        return MIN_ANGLE
    if angle > MAX_ANGLE:
        return MAX_ANGLE
    return angle


def execute_pan_angle(board: pymata4.Pymata4, angle: int):
    current_pan_angle = angle
    board.servo_write(SERVO_PAN_PIN, clamp_angle(angle))


def times_list(l: List[float], co: float) -> List[float]:
    return [ele * co for ele in l]


board = pymata4.Pymata4()

current_pan_angle = 90
current_tilt_angle = 90

for pin in DIRA_PINS:
    board.set_pin_mode_digital_output(pin)

for pin in DIRB_PINS:
    board.set_pin_mode_digital_output(pin)

for pin in PWM_PINS:
    board.set_pin_mode_pwm_output(pin)

board.set_pin_mode_servo(SERVO_PAN_PIN)
board.set_pin_mode_servo(SERVO_TILT_PIN)


# print(board.get_firmata_version())

# execute_movement_vector(board, [-2.0, 2.0, -2.0, 2.0])

execute_movement_vector(board, times_list([-1, -1, 1, 1], 2))

sleep(5)

execute_movement_vector(board, [0.0, 0.0, 0.0, 0.0])

# board.set_pin_mode_servo(SERVO_PAN_PIN)

# angle = 45
# while angle <= 135:
#     board.servo_write(SERVO_PAN_PIN, angle)
#     angle += 1
#     sleep(0.1)


board.shutdown()
