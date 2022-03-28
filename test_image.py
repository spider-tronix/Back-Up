from tf_pose import common
import cv2
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import numpy as np

def get_coordinates(image):
    # Fix the image dimensions to 432x368
    w, h = model_wh('432x368')
    
    e = TfPoseEstimator(get_graph_path('cmu'), target_size=(w, h))
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)
    output_image = TfPoseEstimator.draw_humans(np.zeros(image.shape), humans, imgcopy=False)
    #output_image = cv2.resize(output_image,dsize=(432,368))
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

input_image = common.read_imgfile("/home/adarsh/projects/sangam-backup/demo/WhatsApp Image 2022-03-19 at 11.16.21 AM.jpeg", None, None)
print(input_image.shape)
output_image, coordinates = get_coordinates(input_image)
cv2.imshow('Image', output_image)
cv2.waitKey(0)
