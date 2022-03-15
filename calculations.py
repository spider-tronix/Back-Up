from mimetypes import init
from image_process import get_coordinates, feed_input
import math
import numpy as np

input_image = feed_input('demo_image')
output_image, output_coordinates = get_coordinates(input_image)
n_ppl = len(output_coordinates)

def init_coordinates(output_coordinates, person):
    coordinates = {}

    coordinates['nose'] = (output_coordinates[person][0][1],output_coordinates[person][0][2])
    coordinates['neck'] = (output_coordinates[person][1][1],output_coordinates[person][1][2])
    coordinates['right_shoulder'] = (output_coordinates[person][2][1],output_coordinates[person][2][2])
    coordinates['left_shoulder'] = (output_coordinates[person][5][1],output_coordinates[person][5][2])
    coordinates['right_hip'] = (output_coordinates[person][8][1],output_coordinates[person][8][2])
    coordinates['left_hip'] = (output_coordinates[person][11][1],output_coordinates[person][11][2])
    coordinates['centre_hip'] = ((coordinates['right_hip'][0] + coordinates['right_hip'][1])/2, 
                                 (coordinates['left_hip'][0] + coordinates['left_hip'][1])/2)

    if coordinates['nose'][0] > coordinates['neck'][0]:
        paral_x = coordinates['neck'][0] + 30
    else:
        paral_x = coordinates['neck'][0] - 30
    paral_y = coordinates['neck'][1]
    coordinates['collar_parallel'] = (paral_x,paral_y)

    if coordinates['neck'][0] > coordinates['centre_hip'][0]:
        hparal_x = coordinates['centre_hip'][0] + 30
    else:
        hparal_x = coordinates['centre_hip'][0] - 30
    hparal_y = coordinates['centre_hip'][1]
    coordinates['hip_parallel'] = (hparal_x,hparal_y)

    return coordinates

def anglecalc(coordinates, part1, part2, part3):
    x1,y1 = coordinates[part1]
    x2,y2 = coordinates[part2]
    x3,y3 = coordinates[part3]

    p1 = np.array([x1,y1]) - np.array([x2,y2])
    p2 = np.array([x3,y3]) - np.array([x2,y2])
    cosine_angle = np.dot(p1, p2) / (np.linalg.norm(p1) * np.linalg.norm(p2))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)

def distance(coordinates, part1, part2):
    x1,y1 = coordinates[part1]
    x2,y2 = coordinates[part2]
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return dist

def calc_parameters(coordinates):
    param = {}
    param['n_ppl'] = n_ppl

    shoulder_width = coordinates['left_shoulder'][0] - coordinates['right_shoulder'][0]
    param['X_left'] = coordinates['neck'][0] - 0.65*shoulder_width
    param['X_right'] = coordinates['neck'][0] + 0.65*shoulder_width

    param['torso_angle'] = anglecalc(coordinates,'neck','left_hip', 'right_hip')
    param['spine_length'] = distance(coordinates,'neck','centre_hip')
    param['neck_angle'] = anglecalc(coordinates,'nose','neck','collar_parallel')
    param['back_angle'] = anglecalc(coordinates,'neck','centre_hip','hip_parallel')
    param['nose_to_hip_length'] = distance(coordinates,'nose','centre_hip')
    param['Y_up'] = coordinates['nose'][1]
    param['Y_down'] = (coordinates['neck'][1] + coordinates['centre_hip'][1])/2
    
    return param