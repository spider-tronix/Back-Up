from cmath import pi
from tf_pose import common
import cv2
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import matplotlib.pyplot as plt
import numpy as np

def anglecalc(keypoint_list,n1,n2,n3):
    
    _,x1,y1 = keypoint_list[n1]
    _,x2,y2 = keypoint_list[n2]
    _,x3,y3 = keypoint_list[n3]

    p1 = np.array([x1,y1]) - np.array([x2,y2])
    p2 = np.array([x3,y3]) - np.array([x2,y2])
    cosine_angle = np.dot(p1, p2) / (np.linalg.norm(p1) * np.linalg.norm(p2))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)

if __name__ == '__main__':

    image = 'demo/WhatsApp Image 2022-02-23 at 12.14.55 PM.jpeg'       # image path
    image = common.read_imgfile(image, None, None)
    w, h = model_wh('432x368')       # image resolution - fix at 432x368

    e = TfPoseEstimator(get_graph_path('cmu'), target_size=(w, h))
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)
    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
    image = cv2.resize(image,dsize=(432,368))

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

    #print(people_coordinates)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    angle = anglecalc(people_coordinates['Person1'],8,1,11)
    print(angle)
    plt.show()