from tf_pose import common
import cv2
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import matplotlib.pyplot as plt
import base64
import numpy as np
import paho.mqtt.client as mqtt
from queue import Queue
import socket

def get_coordinates(image):
    # Fix the image dimensions to 432x368
    w, h = model_wh('432x368')
    
    e = TfPoseEstimator(get_graph_path('cmu'), target_size=(w, h))
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)
    output_image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
    output_image = cv2.resize(image,dsize=(432,368))
    coordinates_unsorted = {}
    for i,human in enumerate(humans):
        coordinates = []
        for j in human.body_parts:
            x = round(human.body_parts[j].x*w,2)
            y = round(human.body_parts[j].y*h,2)
            coordinates.append((j,x,y))
        coordinates_unsorted['person'+str(i+1)] = coordinates
    coordinates_unsorted = dict(sorted(coordinates_unsorted.items(), key=lambda item: item[1][0][1]))
    
    ouput_coordinates = {}
    for k in range(0,len(coordinates_unsorted)):
        ouput_coordinates['Person'+str(k+1)] = coordinates_unsorted[str(list(coordinates_unsorted.items())[k][0])]

    return output_image,ouput_coordinates

MQTT_RPI_IMG_RCV = "home/rpi1/images"
MQTT_RPI_FRM_ITL_SEND = "home/rpi1/startstream"
MQTT_SERVER = socket.gethostbyname(socket.gethostname())

def feed_input(mode,img_path):
    input_image = np.zeros((5,4,3))
    
    if mode == 'webcam':
        cam = cv2.VideoCapture(0)
        res, input_image = cam.read()
    
    elif mode == 'demo_image':
        input_image_path = img_path
        input_image = common.read_imgfile(input_image_path, None, None)
    
    elif type(mode) == list and mode[0] == 'rpi':
        #send frame interval -1 for stop streaming
        #send frame interval as a +ve no. x for the rpi to send continuous frames separated by x seconds
        #send frame interval -2 for requesting for a single image
        client = mode[1]
        image_queue = mode[2]
        client.publish(MQTT_RPI_FRM_ITL_SEND, -2)
        image_queue.queue.clear()
        input_image = image_queue.get()
        while not image_queue.empty():
            input_image = image_queue.get()
        
    
    elif type(mode) == list and mode[0] == 'rpi_calib':
        client = mode[1]
        image_queue = mode[2]
        while True:
            client.publish(MQTT_RPI_FRM_ITL_SEND, -2)
            image_queue.queue.clear()
            input_image = image_queue.get()
            while not image_queue.empty():
                input_image = image_queue.get()
            cv2.imshow('Calibration Preview', input_image)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                break
        #client.publish(MQTT_RPI_FRM_ITL_SEND, -1)

    else:
        print('Incorrect input mode')

    return input_image

def initRPiCommClient():

    image_queue = Queue(maxsize = 1)

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(MQTT_RPI_IMG_RCV)

    def rpi_image_callback(client, userdata, msg):
        nonlocal image_queue
        img = base64.b64decode(msg.payload)
        npimg = np.frombuffer(img, dtype=np.uint8)
        frame = cv2.imdecode(npimg, 1)
        if not image_queue.full():
            image_queue.put(frame)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(MQTT_SERVER)
    client.message_callback_add(MQTT_RPI_IMG_RCV, rpi_image_callback)

    return client, image_queue

def testing():
    input_image = feed_input('demo_image','demo/Employees-working-collaboratively-in-an-open-floor-plan-office-1.jpg')
    out_image,coordinates = get_coordinates(input_image)
    plt.imshow(cv2.cvtColor(out_image, cv2.COLOR_BGR2RGB))
    plt.show()
    #print(coordinates)