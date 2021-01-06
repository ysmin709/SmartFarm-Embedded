#!/usr/bin/python3
import socket
import os

try:  # 연결에 성공한 경우
    gw = os.popen("ip -4 route show default").read().split()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((gw[2], 0))
    print("Connection Success!")
    # ipaddr = s.getsockname()[0]
    # gateway = gw[2]
    # host = socket.gethostname()
    # print("IP:", ipaddr, " GW:", gateway, " Host:", host)
except:  # 연결에 실패한 경우 Wifi를 설정한다.
    print("No Connection!!")
    cmd = "chmod +x /home/pi/Desktop/SetWifiCommand.py"
    run_cmd = "./SetWifiCommand.py"
    # Wifi 최종 설정을 위해 reboot 필요. autostart 파일에 등록시 무한 reboot 문제 발생 가능성 있음.
    # reboot_cmd = "sudo reboot"

    os.system(cmd)
    os.system(run_cmd)
    # os.system(reboot_cmd)
