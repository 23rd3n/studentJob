#!/usr/bin/env python3
import json
import requests
import time
import threading
import argparse


headers = {"content-type": "application/json"}

def signal_handler(signal, frame):
    global stop_signal
    stop_signal=True
    time.sleep(0.5)
    exit() 

stop_signal = False

def make_prediction(url, data, headers):
    json_response = requests.post(url, data=data, headers=headers)
    predictions = json_response.json()['predictions'][0]
    return predictions

def perform_prediction(url, data, headers):
    global stop_signal
    while not stop_signal:
        result = make_prediction(url, data, headers)
    return result

def main(num_threads):
    global stop_signal
    print("Running...")
    with open('./data_cam12.json') as f:
        data_cam12 = json.load(f)
    
    url2 = ''

    threads = []


    for _ in range(num_threads):
        t = threading.Thread(target=perform_prediction, args=(url2, data_cam12, headers))
        t.start()
        threads.append(t)
    
    
    while not stop_signal:
        start_time = time.time()
        make_prediction(url2, data_cam12, headers)
        end_time = time.time()
        delay = end_time - start_time  # Calculate the elapsed time
        print(f"URL2 w/ {num_threads+1} procs |  Delay = {delay*1000} ms | ")  
        #print("(#proc: ",num_threads,"| Delay = ",round(delay * 1000), "ms |)")  # Print the delay

    # Wait for all threads to complete
    stop_signal = True
    for t in threads:
        t.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_threads", type=int, default=0, help="Number of threads to create || default just main")
    args = parser.parse_args()

    main(args.num_threads)
