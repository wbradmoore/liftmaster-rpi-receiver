#!/usr/bin/python3

import time, datetime, requests, json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

with open('webhooks.json') as infile:
    webhooks = json.load(infile)

print(webhooks)

debounce_seconds = 1
last_press = {2:0,3:0,4:0}

def handler(pin):
    # global last_press
    if time.time() - last_press[pin] > debounce_seconds:
        last_press[pin]=time.time()
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" Button Press "+str(pin))
        resp=requests.post(webhooks[str(pin)])
        print(resp)
    time.sleep(.25)

GPIO.add_event_detect(2, GPIO.FALLING, handler)
GPIO.add_event_detect(3, GPIO.FALLING, handler)
GPIO.add_event_detect(4, GPIO.FALLING, handler)


while True:
    #heartbeat
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" Heartbeat")
    resp=requests.post(webhooks["heartbeat"])
    print(resp)
    time.sleep(60*60)
