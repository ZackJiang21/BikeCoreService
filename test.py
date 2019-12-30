from core.lib import HKIPcamera3
from core.lib import HKIPcamera2
from core.lib import HKIPcamera1
import numpy as np

import cv2



ip1 = str('10.90.90.91')  #摄像头IP地址，要和本机IP在同一局域网
ip2 = str('10.90.90.92')
ip3 = str('10.90.90.93')


name = str('admin')       #管理员用户名
pw = str('shihang123')      #管理员密码
HKIPcamera3.init(ip3, name, pw)
HKIPcamera2.init(ip2, name, pw)
HKIPcamera1.init(ip1, name, pw)
while True:
    fram1 = HKIPcamera1.getframe()
    fram2 = HKIPcamera2.getframe()
    fram3 = HKIPcamera3.getframe()
    frame1 = cv2.pyrDown(np.rot90(np.array(fram1)))
    frame2 = cv2.pyrDown(np.rot90(np.array(fram2)))
    frame3 = cv2.pyrDown(np.rot90(np.array(fram3)))
    cv2.imshow('show_img1', frame1)
    cv2.imshow('show_img2', frame2)
    cv2.imshow('show_img3', frame3)
    cv2.waitKey(1)
#HKIPcamera.release()
#time.sleep(5)
