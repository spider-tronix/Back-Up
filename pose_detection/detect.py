from cv2 import KeyPoint
from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import matplotlib.pyplot as plt

if __name__ == '__main__':

    image = 'demo/demo_99.png'       # image path
    w, h = model_wh('432x368')       # image resolution

    e = TfPoseEstimator(get_graph_path('cmu'), target_size=(w, h))
    image = common.read_imgfile(image, None, None)
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

    people_new = {}

    for k in range(0,len(people)):
        temp = people[str(list(people.items())[k][0])]
        people_new['Person'+str(k+1)] = temp

    print(people_new)

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()