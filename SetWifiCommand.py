#!/usr/bin/sudo /usr/bin/python3
import os

testid = input("id: ")
testpassword = input("password: ")
test = "network={\n    ssid=\"%s\"\n    psk=\"%s\"\n    key_mgmt=WPA-PSK\n}\n"%(testid, testpassword)
f = open("/etc/wpa_supplicant/wpa_supplicant.conf", 'a+')
f.write(test)
f.close()
