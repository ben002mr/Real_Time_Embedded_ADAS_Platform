import cv2
from picamera2 import Picamera2
import serial
import time

# Serial connection to NodeMCU
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)

# Load face detector
face_cascade = cv2.CascadeClassifier(
    '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
)

# Initialize Pi Camera
picam2 = Picamera2()

picam2.configure(
    picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    )
)

picam2.start()

print("Mini ADAS Fusion System Started")

frame_count = 0

# Keep previous FCW state
fcw_status = "SAFE"

while True:

    # Capture frame
    frame = picam2.capture_array()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Face detection
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    # Read ALL available serial data
    while ser.in_waiting > 0:

        line = ser.readline().decode('utf-8').strip()

        if line == "SAFE":
            fcw_status = "SAFE"

        elif line == "WARNING":
            fcw_status = "WARNING"

        elif line == "DANGER":
            fcw_status = "DANGER"

    # Driver status logic
    if len(faces) > 0:
        driver_status = "NORMAL"
    else:
        driver_status = "NO DRIVER"

    # Console output
    print(
        f"Faces: {len(faces)} | "
        f"FCW: {fcw_status} | "
        f"STATUS: {driver_status}"
    )

    # Save debug image every 100 frames
    frame_count += 1

    if frame_count % 100 == 0:

        filename = f"fusion_frame_{frame_count}.jpg"

        cv2.imwrite(filename, frame)

        print(f"Saved: {filename}")

    time.sleep(0.1)
