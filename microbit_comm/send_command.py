import serial

def send_command(cmd):
    with serial.Serial('COM3', 115200, timeout=1) as ser:  # Update COM port
        ser.write(cmd.encode())