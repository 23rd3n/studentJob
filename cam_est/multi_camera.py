import pyzed.sl as sl
import cv2
import numpy as np
import threading
import time
import signal
import json
import requests

################################## USER DEFINED ##################################

url1 = 'http://10.162.148.140:8501/v1/models/serkut_peach:predict'
headers = {"content-type": "application/json"}
fps = 15 
fps_fac = 1/5
sub_more = 2
sub_frt = 3


cropwidthbeg_cam2 = 90 # 0
cropwidthend_cam2 = 490 # 640
cropheightbeg_cam2 = 20 # 0
cropheightend_cam2 = 360 # 360


def prepare_peach_img_cam(img,sub_more,sub_frt,cropwidthbeg_cam2,cropwidthend_cam2,cropheightbeg_cam2,cropheightend_cam2):
   peach_img_pre = img[::sub_more,::sub_more]
   peach_img_pre2 = peach_img_pre[cropheightbeg_cam2:cropheightend_cam2:sub_frt,cropwidthbeg_cam2:cropwidthend_cam2:sub_frt]
   peach_img = peach_img_pre2.astype('float16')
   peach_img *= 1.0/255.0
   return peach_img


def make_prediction(url,data, headers):
   json_response = requests.post(url, data=data, headers=headers)
   predictions = json_response.json()['predictions'][0]

################################## USER DEFINED ##################################   

zed_list = []
left_list = []
depth_list = []
timestamp_list = []
im_peach_list = []
thread_list = []
stop_signal = False
cam1 = 25306655
cam2 = 26323710
im_peach1 = []
im_peach2 = []

def signal_handler(signal, frame):
    global stop_signal
    stop_signal=True
    time.sleep(0.5)
    exit()

def grab_run(index,cameras):
    global stop_signal
    global zed_list
    global timestamp_list
    global left_list
    global depth_list
    global im_peach1
    global im_peach2


    runtime = sl.RuntimeParameters()
    runtime.sensing_mode = sl.SENSING_MODE.FILL
    while not stop_signal:
        #This function will grab the latest images from the camera, 
        #rectify them, and compute the measurements based on the 
        #RuntimeParameters provided (depth, point cloud, tracking, etc.) 
        err = zed_list[index].grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            zed_list[index].retrieve_image(left_list[index])
            zed_list[index].retrieve_measure(depth_list[index], sl.MEASURE.DEPTH)
            #print(depth_list[index].get_data().shape) #(720, 1280)
            # if (cameras[index].serial_number == cam1):
            #     #print("here1")
            #     im_pre1=depth_list[index].get_data()
            #     im_peach1 = prepare_peach_img_cam(im_pre1,sub_more,sub_frt,cropwidthbeg_cam2,cropwidthend_cam2,cropheightbeg_cam2,cropheightend_cam2)
            # else:
            #     #print("here2")
            #     im_pre2=depth_list[index].get_data()
            #     im_peach2 = prepare_peach_img_cam(im_pre2,sub_more,sub_frt,cropwidthbeg_cam2,cropwidthend_cam2,cropheightbeg_cam2,cropheightend_cam2)
            timestamp_list[index] = zed_list[index].get_timestamp(sl.TIME_REFERENCE.CURRENT).data_ns
        time.sleep(0.001) #1ms
    zed_list[index].close()
	
def main():
    global stop_signal
    global zed_list
    global left_list
    global depth_list
    global timestamp_list
    global thread_list
    global im_peach1
    global im_peach2
    signal.signal(signal.SIGINT, signal_handler)

    print("Running...")
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.camera_fps = fps  # The framerate is lowered to avoid any USB3 bandwidth issues
    init.depth_mode = sl.DEPTH_MODE.ULTRA # sl.DEPTH_MODE.NONE, PERFORMANCE, ULTRA, QUALITY

    #List and open cameras
    name_list = []
    last_ts_list = []

    #This function lists all the cameras available and 
    #provides their serial number, models and other information. 
    cameras = sl.Camera.get_device_list()
    #print(cameras)

    index = 0

    for cam in cameras:
        # loop for the cameras
        init.set_from_serial_number(cam.serial_number)

        #name_list'e kamera'nin id'sini ekle
        name_list.append("ZED {}".format(cam.serial_number))
        print("Opening {}".format(name_list[index]))

        #yeni bir Camera nesnesi tanimla ve liste ekle  
        zed_list.append(sl.Camera())

        #kamera'nin bir lensi left image digeri depth image
        # sl.Mat() image matrisleri
        left_list.append(sl.Mat())
        depth_list.append(sl.Mat())

        #initialize two lists with values of 0 that 
        #will later be used for synchronizing the camera streams.
        timestamp_list.append(0)
        last_ts_list.append(0)

        #kamera'yi acmaya calis acamazsan hata'yi goruntule
        status = zed_list[index].open(init)
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            zed_list[index].close()
        index = index +1

    #Start camera threads
    for index in range(0, len(zed_list)):
        if zed_list[index].is_opened():
            thread_list.append(threading.Thread(target=grab_run, args=(index, cameras,)))
            thread_list[index].start()
    
    #Display camera images
    key = ''
    flag = 0
    while key != 113:  # for 'q' key
        for index in range(0, len(zed_list)):
            if zed_list[index].is_opened():
                if (timestamp_list[index] > last_ts_list[index]):
                    cv2.imshow(name_list[index], left_list[index].get_data())
                    x = round(depth_list[index].get_width() / 2) #width of depth matrix
                    y = round(depth_list[index].get_height() / 2) #height of depth matrix
                    err, depth_value = depth_list[index].get_value(x, y) #ortanin depth'i
                    if np.isfinite(depth_value):
                        print("{} depth at center: {}MM".format(name_list[index], round(depth_value)))
                    last_ts_list[index] = timestamp_list[index]
        
        # if zed_list[0].is_opened() and zed_list[1].is_opened():
        #     if len(im_peach1) > 0 and len(im_peach2) > 0:
        #         print(" They're being written to JSON...")
        #         data_cam12 = json.dumps({"instances": [{'input_156':im_peach1.to_list(),
        #                                                 'input_157':im_peach2.to_list()}]})
        #         result1 = make_prediction(url1,data_cam12, headers)
        #         flag+=1
        #         f = open("/home/lkn/OPs/bothCamEst.txt", "w")
        #         result1_formatted = [f"{num:.4f}" for num in result1] #4 DIGITS, STRINGS
        #         result1_str = " ".join(result1_formatted) #BIRBIRLERINE BIR BOSLUK BIRAKARAK EKLE
        #         f.write(str(flag)+"\n"+result1_str) 
        #         f.close()

        key = cv2.waitKey(10)
    cv2.destroyAllWindows()

    #Stop the threads
    stop_signal = True
    for index in range(0, len(thread_list)):
        thread_list[index].join()

    print("\nFINISH")

if __name__ == "__main__":
    main()