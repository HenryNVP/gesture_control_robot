from yolo_hand_gesture.detect_gesture import detect
from microbit_comm.send_command import send_command
import json

with open('microbit_comm/command_map.json') as f:
    command_map = json.load(f)

def main():
    gesture = detect()
    if gesture in command_map:
        cmd = command_map[gesture]
        send_command(cmd)