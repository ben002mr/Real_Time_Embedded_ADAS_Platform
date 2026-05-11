import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600)

time.sleep(2)

print("Mini ADAS Serial Monitor Started")

while True:

    if ser.in_waiting > 0:

        line = ser.readline().decode('utf-8').rstrip()

        print(line)