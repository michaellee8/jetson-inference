from typing import List
from pymata4 import pymata4
from time import sleep
from math import floor
from enum import Enum
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
RIGHT_SONIC_TRIG_PIN = 61  # A7 PF7




NORMAL_PWM = 100

BACKGROUND = 0
background = 1
car = 2
sonic = 3
wheel = 4
santa = 5
wheel_back = 6
santa_back = 7

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

parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", \
    formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +\
    jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

# python3 detectnet_20210723_USB.py --model=$NET/ssd-mobilenet.onnx --label=$NET/labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes --input_URI=csi://0

#More arguments (For commandline arguments)
parser.add_argument("input_URI", type=str, default="csi://0", nargs='?', help="URI of the input stream")

parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.3, help="minimum detection threshold to use") 

#Print help when no arguments given
try:
    opt = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)

print("capturing", opt.input_URI)

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
# output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)

print("got video source")

cam_height = input.GetHeight()
cam_width = input.GetWidth()

print("cam w h", cam_width, cam_height)

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

def execute_tilt_angle(board: pymata4.Pymata4, angle: int):
    current_tilt_angle = angle
    board.servo_write(SERVO_TILT_PIN, clamp_angle(angle))


def times_list(l: List[float], co: float) -> List[float]:
    return [ele * co for ele in l]


board = pymata4.Pymata4(arduino_instance_id=2)

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
board.set_pin_mode_sonar(LEFT_SONIC_TRIG_PIN, LEFT_SONIC_ECHO_PIN)
board.set_pin_mode_sonar(RIGHT_SONIC_TRIG_PIN, RIGHT_SONIC_ECHO_PIN)

# [START] prep done
#######################################
# Main code start
#######################################


# print(board.get_firmata_version())

# execute_movement_vector(board, [-2.0, 2.0, -2.0, 2.0])

# execute_movement_vector(board, times_list([-1, -1, 1, 1], 2))

# sleep(5)

# execute_movement_vector(board, [0.0, 0.0, 0.0, 0.0])

# board.set_pin_mode_servo(SERVO_PAN_PIN)

# angle = 45
# while angle <= 135:
#     board.servo_write(SERVO_PAN_PIN, angle)
#     angle += 1
#     sleep(0.1)


class Side(Enum):
    NONE: str = "none"
    LEFT: str = "left"
    RIGHT: str = "right"

last_seen_car_side: Side = Side.NONE
last_seen_car_direction: Side = Side.NONE

while True:

    img = input.Capture()
    detections = net.Detect(img, overlay=opt.overlay)
    car_det = 
        
    
    sleep(1)
    # left_dist = board.sonar_read(LEFT_SONIC_TRIG_PIN)
    # right_dist = board.sonar_read(RIGHT_SONIC_TRIG_PIN)
    # print("left: ", left_dist, ", right: ", right_dist)
    # sleep(5)


board.shutdown()
