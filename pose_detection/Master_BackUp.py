import time
print("Clear data(y/n)?")
resp = input()
if(resp == "y"):
    print("Clearing......")
    import clear_data
print("Sit erect for calibration...")
print("Calibrating in....")
time.sleep(1)
print("3...")
time.sleep(1)
print("2...")
time.sleep(1)
print("1...")
time.sleep(1)
print("Intializing calibration...")
import Calibrate_BackUp_combined
print("Calibration successful...")
i = input("Press Enter to continue: ")
print("Checking posture....")
import Check_backup_combined
print("Posture check successful....")
print("Sending notifications.....")
import Push_notification