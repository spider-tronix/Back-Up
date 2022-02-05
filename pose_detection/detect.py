from cv2 import KeyPoint
from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

if __name__ == '__main__':

    image = 'demo/demo_1.jpeg'
    w, h = model_wh('432x368')

    if w == 0 or h == 0:
        e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))
    else:
        e = TfPoseEstimator(get_graph_path('cmu'), target_size=(w, h))

    image = common.read_imgfile(image, None, None)
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)

    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

    '''cv2.imshow('result',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''

    people = {}

    for i,human in enumerate(humans):

        people['Person'+str(i+1)] = human

    print(people)