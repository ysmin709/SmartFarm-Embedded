# SmartFarm-Embedded

## Setting
#### PH, EC, RTD, CO2, HUM, PMP Sensor Module UART to I2C : https://www.instructables.com/UART-AND-I2C-MODE-SWITCHING-FOR-ATLAS-SCIENTIFIC-E/
* pH, EC, RTD Sensor들의 통신 변경 방법과 CO2, HUM, PMP Sensor의 통신 변경 방법이 다르므로, 위의 링크에서 "Step 2: MANUAL SWITCHING" 그림을 주의하여 참고한다. 
#### Raspberry Pi I2C Setting : https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
#### Autostart
  - Sensor 폴더 안에 autostartWifi.sh Shellscript 파일 생성
    #!/bin/sh
    cd Desktop/Sensor
    python3 SetWifi.py
    python3 test.py
  - 터미널을 열고 sudo nano /etc/xdg/lxsession/LXDE-pi/autostart 입력
  - @pcmanfm와 @xscreensaver 사이에 lxterminal -e /home/pi/Desktop/Sensor/autostartWifi.sh 입력 후 저장
  - Reboot를 진행하여 잘 작동하는지 확인

#### Wifi
  - Raspberry Pi에서 Wifi에 관한 정보는 "wpa_supplicant.conf"파일에 있다.
  - 현재 Raspberry Pi 실행시 id와 pw를 입력하면 "wpa_supplicant.conf"파일에 입력 정보가 저장된다.
  - "wpa_supplicant.conf"파일은 읽기 전용 파일이므로 관리자 모드로 실행해야한다.
  - 같은 Wifi를 사용하는 경우 id와 pw를 한번만 입력하면 이후에 부팅할때마다 입력없이 자동으로 Wifi에 연결된다.
  - ##### 주의 사항
    - id와 pw 입력시 id는 정확하게 입력했으나 pw를 잘못 입력하는 경우 재부팅이 되어도 Wifi에 연결되지 않는다.
    - 이런 경우, "wpa_supplicant.conf"파일을 실행하여 해당 network(id, pw)를 지우고 재부팅한다. 이후, id와 pw를 다시 정확하게 입력한다.
    - 위와 같은 문제를 해결하기 위해 각 네트워크마다 우선순위를 부여하는 방법을 찾았으나 구현에 어려움이 있어 추후 개발이 필요하다.
    - wpa_supplicant 파일 관련 링크: https://acertainlog.wordpress.com/2015/06/21/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC-%ED%8C%8C%EC%9D%B4%EC%9D%98-%ED%84%B0%EB%AF%B8%EB%84%90%EC%97%90%EC%84%9C-wifi-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0/
    - 네트워크 우선순위 관련 링크: https://m.blog.naver.com/21ahn/221308950395
