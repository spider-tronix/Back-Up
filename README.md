# Back-Up
This repo uses a tensorflow implementation of OpenPose model to detect human pose and to find out if they are slouching (sitting in an abrupt or wrong posture) while sitting and working at their desks.
- Can detect multiple people in a single frame
- Can even detect if people are sitting sideways and detects slouching accordingly
- Sends a push notification using PushBullet if they are found to be sitting in a wrong posture
- Maintaining an excel database using Openpyxl library

**Note:** To run this repo, donwload pre-trained weights from https://drive.google.com/file/d/1ssD26Z1NA5IV8h6yIR5FtEEsPs6xCFlj/view?usp=sharing and move to /models/graph/cmu
