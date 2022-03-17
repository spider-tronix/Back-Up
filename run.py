from image_process import get_coordinates, feed_input
from clear_data import clear
from calibrate import calibrate_write_excel
from checkslouch import slouch_detect_write_excel
from push_notification import push_notify

file_name = "Back-Up API person data.xlsx"
clear(file_name)

input_image = feed_input('demo_image','demo/2022-03-17-002453.jpg')
output_image,output_coordinates = get_coordinates(input_image)
calibrated_params = calibrate_write_excel(output_coordinates,file_name)

input_image = feed_input('demo_image','demo/2022-03-17-002503.jpg')
output_image,output_coordinates = get_coordinates(input_image)
slouch_detect_write_excel(calibrated_params,output_coordinates,file_name)

push_notify()