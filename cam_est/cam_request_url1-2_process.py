#!/usr/bin/env python3
import pyzed.sl as sl
import cv2
import time
import signal
import json
import requests
import multiprocessing as mp

def prepare_peach_img_cam(img):
   sub_more = 2
   sub_frt = 3
   cropwidthbeg_cam2 = 90 # 0
   cropwidthend_cam2 = 490 # 640
   cropheightbeg_cam2 = 20 # 0
   cropheightend_cam2 = 360 # 360
   peach_img_pre = img[::sub_more,::sub_more,:]
   peach_img_pre2 = peach_img_pre[cropheightbeg_cam2:cropheightend_cam2:sub_frt,cropwidthbeg_cam2:cropwidthend_cam2:sub_frt]
   peach_img = peach_img_pre2.astype('float16')
   peach_img *= 1.0/255.0
   return peach_img

def make_prediction_timely_url1(data,node_id):
    url1 = '' # insert url1 here
    headers = {"content-type": "application/json"}

    start_time = time.time()  # Start the timer

    json_response = requests.post(url1, data=data, headers=headers)
    predictions = json_response.json()['predictions'][0]

    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    print("Time for response, by URL 1:",round(elapsed_time*1000), "ms ")
    delay_json1 = {"url_1": {"node_id": node_id, "average_ms":elapsed_time*1000 }}
    with open('./json_url1.json', 'w') as f1:
        json.dump(delay_json1, f1)

    with open("./url1_estimate.txt", "w") as txtYaz:
        result1_formatted = [f"{num:.4f}" for num in predictions] #4 DIGITS, STRINGS
        result1_str = " ".join(result1_formatted) #BIRBIRLERINE BIR BOSLUK BIRAKARAK EKLE
        txtYaz.write(str(node_id)+"\n"+result1_str)

    return predictions

# same with the url1 for the time-being
def make_prediction_timely_url2(data, node_id): 
    url2 = '' # insert url2 here
    headers = {"content-type": "application/json"}

    start_time = time.time()  # Start the timer

    json_response = requests.post(url2, data=data, headers=headers)
    predictions = json_response.json()['predictions'][0]

    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    print("Time for response, by URL 2:",round(elapsed_time*1000), "ms ")
    delay_json2 = {"url_2": {"node_id": node_id, "average_ms":elapsed_time*1000 }}
    with open('./json_url2.json', 'w') as jsonYAZ:
        json.dump(delay_json2, jsonYAZ)

    with open("./url2_estimate.txt", "w") as txtYaz:
        result1_formatted = [f"{num:.4f}" for num in predictions] #4 DIGITS, STRINGS
        result1_str = " ".join(result1_formatted) #BIRBIRLERINE BIR BOSLUK BIRAKARAK EKLE
        txtYaz.write(str(node_id)+"\n"+result1_str)

    return predictions

def signal_handler(signal, frame):
    global stop_signal
    stop_signal=True
    time.sleep(0.5)
    exit() 

stop_signal = False

def process_url1(data_cam12,lock, node_id):
    prev_id = -1
    while True:
        # wait for the first data_cam
        if node_id.value and node_id.value != prev_id:
            with lock:
                make_prediction_timely_url1(data_cam12.value, node_id.value)
                prev_id = node_id.value

def process_url2(data_cam12,lock, node_id):
    prev_id = -1
    while True:
        # wait for the first data_cam
        if node_id.value and node_id.value != prev_id:
            with lock:
                make_prediction_timely_url2(data_cam12.value, node_id.value)
                prev_id = node_id.value

left_list = []
depth_list = []
name_list = []
zed_list = []

def main():
    global stop_signal
    signal.signal(signal.SIGINT, signal_handler)

    print("Running...")
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.camera_fps = 60  # The framerate is lowered to avoid any USB3 bandwidth issues
    init.depth_mode = sl.DEPTH_MODE.ULTRA # sl.DEPTH_MODE.NONE, PERFORMANCE, ULTRA, QUALITY

    cameras = sl.Camera.get_device_list() # 2 devices

    ## INITIALIZATION OF CAMERAS
    index = 0
    for cam in cameras:
        init.set_from_serial_number(cam.serial_number) #ONEMLI: yoksa kamera baslamaz
        name_list.append("ZED {}".format(cam.serial_number))
        print("Opening {}".format(name_list[index]))
        zed_list.append(sl.Camera())
        left_list.append(sl.Mat())
        depth_list.append(sl.Mat())
        status = zed_list[index].open(init) #kameralari ac
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            zed_list[index].close()
        index = index +1

    
    flag = 0


    # Create a shared memory object for data_cam12 and flag
    manager = mp.Manager()
    data_cam12 = manager.Value('c', '')
    flag = manager.Value('i', 0)
    lock = manager.Lock()

    p1 = mp.Process(target=process_url1, args=(data_cam12, lock, flag))
    p2 = mp.Process(target=process_url2, args=(data_cam12, lock, flag))

    # Start the processes
    p1.start()
    p2.start()

    
    while (not stop_signal):  
        if (zed_list[0].is_opened() and zed_list[1].is_opened()):
            runtime = sl.RuntimeParameters()
            runtime.sensing_mode = sl.SENSING_MODE.FILL
            err0 = zed_list[0].grab(runtime)
            if err0 == sl.ERROR_CODE.SUCCESS:

                    zed_list[0].retrieve_image(depth_list[0], sl.VIEW.DEPTH) 
                    im_pre0=depth_list[0].get_data()
                    im_peach0 = prepare_peach_img_cam(im_pre0[:,:,[0]])

                    # cv2.namedWindow(name_list[0], cv2.WINDOW_NORMAL)
                    # cv2.resizeWindow(name_list[0], 960, 960)
                    # cv2.imshow(name_list[0], im_pre0[:,:,[0]])
                    
            err1 = zed_list[1].grab(runtime)
            if err1 == sl.ERROR_CODE.SUCCESS:

                    zed_list[1].retrieve_image(depth_list[1], sl.VIEW.DEPTH)                
                    im_pre1=depth_list[1].get_data()
                    im_peach1 = prepare_peach_img_cam(im_pre1[:,:,[0]])

                    # cv2.namedWindow(name_list[1], cv2.WINDOW_NORMAL)
                    # cv2.resizeWindow(name_list[1], 960, 960)
                    # cv2.imshow(name_list[1], im_pre1[:,:,[0]])

            with lock:
                data_cam12.value = json.dumps({"instances": [{'input_156': im_peach0.tolist(),
                                                            'input_157': im_peach1.tolist()}]})
                flag.value += 1
                                    

    cv2.destroyAllWindows()
    stop_signal = True
    # Wait for the processes to finish
    p1.terminate()
    p2.terminate()
    zed_list[0].close()
    zed_list[1].close()


if __name__ == "__main__":
    main()
