import cv2
import serial
import time
from picamera2 import Picamera2

# -----------------------------
# SERIAL CONNECTION
# -----------------------------

ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)

# -----------------------------
# CAMERA SETUP
# -----------------------------

picam2 = Picamera2()

picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"

picam2.configure("preview")
picam2.start()

# -----------------------------
# FACE DETECTION
# -----------------------------

face_cascade = cv2.CascadeClassifier(
    '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
)

print("Mini ADAS Headless System Started")

frame_counter = 0

# -----------------------------
# MAIN LOOP
# -----------------------------

while True:

    # Capture frame
    frame = picam2.capture_array()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    # Draw rectangles
    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

    # Read serial data
    sensor_data = "NO DATA"

    if ser.in_waiting > 0:

        sensor_data = ser.readline().decode(
            'utf-8'
        ).rstrip()

    # Console telemetry
    print(
        f"Faces: {len(faces)} | FCW: {sensor_data}"
    )

    # Save frame every 100 loops
    if frame_counter % 100 == 0:

        filename = f"adas_frame_{frame_counter}.jpg"

        cv2.imwrite(filename, frame)

        print(f"Saved: {filename}")

    frame_counter += 1

# -----------------------------
# CLEANUP
# -----------------------------

picam2.stop()
ser.close()
