import cv2
from ultralytics import YOLO

# Load your trained model (update path if needed)
model = YOLO(r"..\yolo_hand_gesture\model\best.pt")

# Open webcam (0 = default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Inference on webcam frame
    results = model(frame)

    # Annotate the results
    annotated_frame = results[0].plot()

    # Display the frame
    cv2.imshow("YOLOv8 - Webcam", annotated_frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
