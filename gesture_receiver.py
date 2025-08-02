import socket
import asyncio
from sphero_sdk import SerialAsyncDal, SpheroRvrAsync

HOST = ''  # Listen on all interfaces
PORT = 5000

gesture_map = {
    "forward": (128, 0, 0),
    "left":    (80, 330, 0),
    "right":   (80, 30, 0),
    "back":    (128, 180, 1),
    "stop":    (0, 0, 0)
}

async def control_rvr(rvr, command):
    speed, heading, flags = gesture_map.get(command, (0, 0, 0))
    await rvr.drive_with_heading(speed, heading, flags)

async def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Listening on port {PORT}...")

    conn, addr = server.accept()
    print(f"Connected by {addr}")

    dal = SerialAsyncDal(asyncio.get_event_loop())
    rvr = SpheroRvrAsync(dal=dal)
    await rvr.wake()
    await rvr.reset_yaw()

    try:
        while True:
            data = conn.recv(1024).decode().strip()
            print("Received:", data)
            if data in gesture_map:
                await control_rvr(rvr, data)
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()
        print("Connection closed.")

if __name__ == "__main__":
    asyncio.run(main())
