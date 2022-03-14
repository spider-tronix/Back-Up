from cgi import test
from tf_pose import common
import cv2
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import matplotlib.pyplot as plt

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

def feed_input(mode):

    if mode == 'webcam':
        cam = cv2.VideoCapture(0)
        res, input_image = cam.read()

    elif mode == 'demo_image':
        input_image_path = 'demo/demo_100.png'
        input_image = common.read_imgfile(input_image_path, None, None)

    elif mode == 'rpi':
        # write code
        pass
    
    elif mode == 'esp32':
        # write code
        pass

    else:
        print('Incorrect input mode')

    return input_image

def testing():

    input_image = feed_input('demo_image')
    out_image,coordinates = get_coordinates(input_image)

    plt.imshow(cv2.cvtColor(out_image, cv2.COLOR_BGR2RGB))
    plt.show()
    print(coordinates)

def covert_to_fisheye():

    from defisheye import Defisheye
    dtype = 'linear'
    format = 'fullframe'
    fov = 180
    pfov = 120

    img = 'demo/WhatsApp Image 2022-02-24 at 5.11.43 PM.jpeg'
    img_out = f"demo/example2_{dtype}_{format}_{pfov}_{fov}.jpg"

    obj = Defisheye(img, dtype=dtype, format=format, fov=fov, pfov=pfov)
    obj.convert(img_out)