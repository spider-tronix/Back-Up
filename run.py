from tkinter import Y
from image_process import get_coordinates, feed_input, initRPiCommClient
from clear_data import clear
from calibrate import calibrate_write_excel
from checkslouch import slouch_detect_write_excel
from push_notification import push_notify
import matplotlib.pyplot as plt
import cv2
import copy
import time

file_name = "Back-Up API person data.xlsx"
print('Calibrate Y|N ?')
res = input()

'''dummyClient, image_queue = initRPiCommClient()
dummyClient.loop_start()'''

if res == 'Y':
    print('Calibrating, sit straight')
    clear(file_name)
    ##input_image_calib = feed_input(['rpi_calib', dummyClient, image_queue], "")
    #input_image_calib = feed_input(['rpi_calib', dummyClient, image_queue], "")
    input_image_calib = feed_input('webcam',0)
    output_image,output_coordinates = get_coordinates(input_image_calib)
    calibrate_write_excel(output_coordinates,file_name)
else:
    pass

while True:
    print('Checking slouching')
    time.sleep(3)
    #input_image_check = feed_input(['rpi', dummyClient, image_queue], "")
    #input_image_check = feed_input(['rpi', dummyClient, image_queue, frame_interval], "")
    #input_image_check = feed_input('demo_image','demo/2022-03-17-002503.jpg')
    input_image_check = feed_input('webcam',0)
    output_image,output_coordinates = get_coordinates(input_image_check)
    #cv2.imshow('check',input_image_check)
    #cv2.waitKey(1)
    slouch_detect_write_excel(output_coordinates,file_name)
    push_notify()
    time.sleep(5)