#!/usr/bin/env python3

import pyzed.sl as sl
import cv2
import numpy as np
import time
import signal
import matplotlib.pyplot as plt
import pyvirtualcam
import sys

fps = 60
fps_fac = 1/5

def signal_handler(signal, frame):
    global stop_signal
    stop_signal=True
    time.sleep(0.5)
    exit() 
    
stop_signal = False
#cam1 = 25306655
#cam2 = 26323710
left_list = []
name_list = []
zed_list = []

def main():
    global stop_signal
    signal.signal(signal.SIGINT, signal_handler)
    print("Running...")
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.camera_fps = fps  # The framerate is lowered to avoid any USB3 bandwidth issues
    init.depth_mode = sl.DEPTH_MODE.ULTRA # sl.DEPTH_MODE.NONE, PERFORMANCE, ULTRA, QUALITY

    #init.set_from_serial_number(cam.serial_number) #there is two cameras?
 
    cameras = sl.Camera.get_device_list() # 2 devices
    #[ZED 2 (0) /dev/video0 SN25306655 AVAILABLE, ZED 2 (1) /dev/video2 SN26323710 AVAILABLE]
    #print(cameras) 

    ## INITIALIZATION OF CAMERAS
    index = 0
    for cam in cameras:
        init.set_from_serial_number(cam.serial_number) #ONEMLI: yoksa kamera baslamaz
        name_list.append("ZED {}".format(cam.serial_number))
        print("Opening {}".format(name_list[index]))
        zed_list.append(sl.Camera())
        left_list.append(sl.Mat())
        status = zed_list[index].open(init) #kameralari ac
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            zed_list[index].close()
        index = index +1



    with pyvirtualcam.Camera(width=1280, height=720, fps=60, device="/dev/video4") as cam1:
        
        with pyvirtualcam.Camera(width=1280, height=720, fps=60, device="/dev/video5") as cam2:

            while (not stop_signal):  # for 'q' key
                if (zed_list[0].is_opened() and zed_list[1].is_opened()):
                    runtime = sl.RuntimeParameters()
                    runtime.sensing_mode = sl.SENSING_MODE.FILL
                    err0 = zed_list[0].grab(runtime)
                    if err0 == sl.ERROR_CODE.SUCCESS: 
                        zed_list[0].retrieve_image(left_list[0], sl.VIEW.LEFT) 
                        rgb_image = cv2.cvtColor(left_list[0].get_data()[:,:,:3], cv2.COLOR_RGB2BGR)
                        cam1.send(rgb_image)      
                    err1 = zed_list[1].grab(runtime)
                    if err1 == sl.ERROR_CODE.SUCCESS:
                        zed_list[1].retrieve_image(left_list[1], sl.VIEW.LEFT)
                        rgb_image = cv2.cvtColor(left_list[1].get_data()[:,:,:3], cv2.COLOR_RGB2BGR)
                        cam2.send(rgb_image)                                           
            stop_signal=True
            zed_list[0].close()
            zed_list[1].close()


if __name__ == "__main__":
    main()
