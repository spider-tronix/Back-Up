from cmath import pi
from tf_pose import common
import cv2
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import matplotlib.pyplot as plt
import numpy as np
import math

def anglecalc(keypoint_list,n1,n2,n3):
    
    _,x1,y1 = keypoint_list[n1]
    _,x2,y2 = keypoint_list[n2]
    _,x3,y3 = keypoint_list[n3]
    p1 = np.array([x1,y1]) - np.array([x2,y2])
    p2 = np.array([x3,y3]) - np.array([x2,y2])
    cosine_angle = np.dot(p1, p2) / (np.linalg.norm(p1) * np.linalg.norm(p2))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def distancecalc(keypoint_list):

    _,x1,y1 = keypoint_list[1]
    _,p1,q1 = keypoint_list[8]
    _,p2,q2 = keypoint_list[11]
    x2,y2 = (p1+p2)/2 , (q1+q2)/2
    dist = math.sqrt((x1-y1)**2 + (x2-y2)**2)
    return dist

def slouchdetect():

    image = 'demo/WhatsApp Image 2022-02-24 at 5.11.42 PM.jpeg'
    image = common.read_imgfile(image, None, None)
    #cam = cv2.VideoCapture(0)
    #res, image = cam.read()

    w, h = model_wh('432x368')
    e = TfPoseEstimator(get_graph_path('cmu'), target_size=(w, h))
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)
    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
    image = cv2.resize(image,dsize=(432,368))

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()

    people = {}
    for i,human in enumerate(humans):
        coordinates = []
        for j in human.body_parts:
            x = round(human.body_parts[j].x*w,2)
            y = round(human.body_parts[j].y*h,2)
            coordinates.append((j,x,y))
        people['person'+str(i+1)] = coordinates

    people = dict(sorted(people.items(), key=lambda item: item[1][0][1]))
    people_coordinates = {}
    for k in range(0,len(people)):
        people_coordinates['Person'+str(k+1)] = people[str(list(people.items())[k][0])]

    output = {}
    for i in range(0,len(people_coordinates)):
        output['Person'+str(i+1)] = (anglecalc(people_coordinates['Person'+str(i+1)],8,1,11), distancecalc(people_coordinates['Person'+str(i+1)]))

    return people_coordinates

op = slouchdetect()
print(op)