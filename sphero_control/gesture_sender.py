import cv2
import socket
from ultralytics import YOLO

# Connect to Raspberry Pi
HOST = '10.0.0.3'  # Replace with your Pi’s IP address
PORT = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Load model
model = YOLO(r"..\yolo_hand_gesture\model\best.pt")

# Start webcam
cap = cv2.VideoCapture(0)
prev_label = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Inference
    results = model(frame)[0]
    annotated = results.plot()

    # Parse results
    for box in results.boxes:
        label_id = int(box.cls[0])
        label = model.names[label_id]
        
        # Only send if different from previous (to reduce spam)
        if label != prev_label:
            print("Sending:", label)
            sock.sendall(label.encode())
            prev_label = label

    # Show window
    cv2.imshow("Gesture", annotated)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
sock.close()
