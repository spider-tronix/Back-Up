from image_process import feed_input, initRPiCommClient
import cv2

dummyClient, image_queue = initRPiCommClient()
dummyClient.loop_start()
frame_interval = 0

input_image_check = feed_input(['rpi', dummyClient, image_queue, frame_interval], "")
#cv2.imwrite('/home/adarsh/projects/sangam-backup/example.jpeg',input_image_check)
cv2.imshow('Received feed', input_image_check)
cv2.waitKey(0)

'''try:
    while True:
        input_image_check = feed_input(['rpi', dummyClient, image_queue, frame_interval], "")
        cv2.imshow('Received feed', input_image_check)
        cv2.waitKey(1)

except:
    dummyClient.disconnect()
'''