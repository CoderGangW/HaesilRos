#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Twist
import serial
import struct

class ArduinoCommunicator:
    def __init__(self):
        rospy.init_node('arduino_controller', anonymous=True)
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # 아두이노의 시리얼 포트
        self.sub = rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)

    def cmd_vel_callback(self, msg):
        # Twist 메시지에서 속도 값을 읽어옴
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        # 아두이노 명령어 포맷에 맞게 변환
        command = self.calculate_command(linear_x, angular_z)
        
        # 아두이노에 명령어 전송
        self.ser.write(command.encode('utf-8'))

    def calculate_command(self, linear_x, angular_z):
        # 선형 속도 및 각속도를 아두이노에 맞는 문자로 변환
        if linear_x > 0:
            return 'w'  # 앞으로
        elif linear_x < 0:
            return 's'  # 뒤로
        elif angular_z > 0:
            return 'd'  # 오른쪽
        elif angular_z < 0:
            return 'a'  # 왼쪽
        else:
            return 'x'  # 정지

if __name__ == '__main__':
    try:
        ArduinoCommunicator()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

