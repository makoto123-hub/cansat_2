import cv2
from picamera2 import Picamera2,Preview
import numpy as np
import RPi.GPIO as GPIO
import time
from gps3 import gps3
from math import radians, sin, con, atan2, sqrt, degrees 

#GPIO,PWM set
GPIO.setmode(GPIO.BCM)

#left
GPIO.setup(18, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

#right
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

left_pwm = GPIO.PWM(18,100)
right_pwm = GPIO.PWM(19,100)

left_pwm.star(0)
right_pwm.star(0)

#camera Setup
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"format": "RGB888"})
picam2.configure(camera_config)
picam2.start()

#Control Parameters
FRAME_CENTER_X = 320
TOLERANCE = 30
SPEED = 50

#gps setup
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

#target setup
TARGET_LATITUDE = 35
TARGET_LONGITUDE = 139

def move_forward(speed):
    left_pwm.ChangeDutyCycle(speed)
    right_pwm.ChangeDutyCycle(speed)

def move_left(speed):
    left_pwm.ChangeDutyCycle(speed)
    right_pwm.ChangeDutyCycle(0)

def move_right(speef):
    left_pwm.ChangeDutyCycle(0)
    right_pwm.ChangeDutyCycle(speed)

def stop():
    left_pwm.ChangeDutyCycle(0)
    right_pwm.ChangeDutyCycle(0)

def calculate_distance_and_bearing(lat1, lon1, lat2, lon2):
    #calculate
    R = 6371000
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon1 - lon2)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    y = sin(d_lon) * cos(radians(lat2))
    x = cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(radians(lat2)) * cos(d_lon)
    bearing = (degrees(atan2(y, x)) + 360) % 360
    return distance, bearing

def get_current_gps():
    for now_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            if data_stream.TPV['lat'] != 'n/a' and data_stream.TPV['lon'] != 'n/a':
                return data_stream.TPV['lat'], data_stream.TPV['lon']

    return None, None

try:
    while True:

        frame = picam2.capture_array()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #red mask
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2

        moments = cv2.moments(mask)
        if moments["m00"] > 0:
            cX = int(moments["m10"] / moments["m00"])

            if abs(cX - FRAME_CENTER_X) < TOLERANCE:
                move_forward(SPEED)
            elif cX < FRAME_CENTER_X:
                turn_left(SPEED)
            elif:
                turn_right(SPEED)

        else:
            stop()

        current_lat, current_lon = get_current_gps()
        if current_lat and current_lon:
            distance, bearing = calculate_distance_and_bearing(current_lat, current_lon, TARGET_LATITUDE, TARGET_LONGITUDE)

            if distance < 2:
                stop()
                break
                
            elif bearing < 45 or bearing > 315:
                move_forward(SPEED)
            elif bearing < 180:
                turn_right(SPEED)
            else:
                turn_left(SPEED)

        result = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow('Red Detection', result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

 finally:
    picam2.close()
    cv2.destroyAllWindows()
    stop()
    GPIO.cleanup()
