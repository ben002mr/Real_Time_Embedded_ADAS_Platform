import cv2
from picamera2 import Picamera2
import serial
import time

# =========================================
# SERIAL CONNECTION TO NODEMCU
# =========================================

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

time.sleep(2)

# =========================================
# LOAD HAAR CASCADES
# =========================================

face_cascade = cv2.CascadeClassifier(
    '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
)

eye_cascade = cv2.CascadeClassifier(
    '/usr/share/opencv4/haarcascades/haarcascade_eye.xml'
)

# =========================================
# INITIALIZE CAMERA
# =========================================

picam2 = Picamera2()

picam2.configure(
    picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    )
)

picam2.start()

print("[INFO] Mini ADAS Main Controller Started")

# =========================================
# VARIABLES
# =========================================

frame_count = 0

fcw_status = "SAFE"

eyes_closed_start = None

drowsy_threshold = 2.0

# =========================================
# MAIN LOOP
# =========================================

while True:

    # =====================================
    # CAPTURE FRAME
    # =====================================

    frame = picam2.capture_array()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # =====================================
    # FACE DETECTION
    # =====================================

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    driver_status = "NO_FACE"

    eye_count = 0

    # =====================================
    # PROCESS FACES
    # =====================================

    for (x, y, w, h) in faces:

        # Face rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Face ROI
        roi_gray = gray[y:y + h, x:x + w]

        roi_color = frame[y:y + h, x:x + w]

        # =================================
        # EYE DETECTION
        # =================================

        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(20, 20)
        )

        eye_count = len(eyes)

        # Draw eye rectangles
        for (ex, ey, ew, eh) in eyes:

            cv2.rectangle(
                roi_color,
                (ex, ey),
                (ex + ew, ey + eh),
                (255, 0, 0),
                2
            )

        # =================================
        # DROWSINESS LOGIC
        # =================================

        if eye_count < 1:

            if eyes_closed_start is None:
                eyes_closed_start = time.time()

            closed_duration = time.time() - eyes_closed_start

            if closed_duration >= drowsy_threshold:

                driver_status = "DROWSY"

            else:

                driver_status = "EYES_CLOSED"

        else:

            eyes_closed_start = None

            driver_status = "ALERT"

    # =====================================
    # SEND DRIVER STATUS TO NODEMCU
    # =====================================

    ser.write((driver_status + "\n").encode())

    # =====================================
    # READ FCW STATUS FROM NODEMCU
    # =====================================

    while ser.in_waiting > 0:

        line = ser.readline().decode('utf-8').strip()

        if line == "SAFE":
            fcw_status = "SAFE"

        elif line == "WARNING":
            fcw_status = "WARNING"

        elif line == "DANGER":
            fcw_status = "DANGER"

    # =====================================
    # SYSTEM FUSION LOGIC
    # =====================================

    if driver_status == "DROWSY" or fcw_status == "DANGER":

        system_status = "DANGER"

    elif fcw_status == "WARNING":

        system_status = "WARNING"

    else:

        system_status = "SAFE"

    # =====================================
    # TERMINAL TELEMETRY
    # =====================================

    print(
        f"Faces: {len(faces)} | "
        f"Eyes: {eye_count} | "
        f"Driver: {driver_status} | "
        f"FCW: {fcw_status} | "
        f"System: {system_status}"
    )

    # =====================================
    # SAVE DEBUG IMAGE
    # =====================================

    if frame_count % 30 == 0:

        filename = f"main_adas_{frame_count}.jpg"

        cv2.imwrite(filename, frame)

        print(f"[INFO] Saved: {filename}")

    frame_count += 1

    # =====================================
    # LOOP DELAY
    # =====================================

    time.sleep(0.1)
