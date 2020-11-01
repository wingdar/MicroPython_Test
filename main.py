import urequests
import network
import time
import machine
from machine import ADC

#import random  #重覆名稱過多，一直無法正常載入

import config

def do_connect():
    # Set to station mode for connecting to network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.SSID, config.PASSWORD)

        # Wait until connected
        while not sta_if.isconnected():
            pass
        print('Network connected!')

def flash_led():
    led = machine.Pin(2, machine.Pin.OUT)
    led.value(0) # In some hardware modules, the on/1 and off/0 is reversed; so here the 0 represents on on my module
    time.sleep(0.5)
    led.value(1)

def get_data():
    # Now dummy, should be retrieved from sensors
    id_num = 2
    #tempx = uniform(2.5, 10.0) #40.1
    #tempx = 40.1
    TMT = ADC(0)
    tempx = TMT.read() / 100
    print('TMT=',tempx)
    
    return (id_num,tempx)
    #return { 'id':id_num,'temp':tempx }
    #return { 'temperature': 25.6 }

def send_data(data):
    print('Sending data...')
    #res = urequests.request("POST","http://192.168.1.218/settemp.php", json=data)
    #res = urequests.put("http://192.168.31.183/settemp.php", json=data)
    res = urequests.put(config.URL, json=data)
    #res = urequests.put("http://192.168.31.183/settemp.php?id={}&temp={}".format(data[0],data[1])) #改成這個模式才能傳，不知道為什麼  
    #res = urequests.put("http://192.168.1.218/settemp.php?id=10&temp=38.5")  #可成功
    print('Response: {}'.format(res.text))
    flash_led() # Indicate successful data transmission

def main():
    # Connect to network
    do_connect()

    # Keep posting sensor data at a certain interval
    while True:
        send_data(get_data())
        time.sleep(10)

main()
