from os import close, times
import serial
import binascii

import time
import sys
import logging
import threading
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_tcp as modbus_tcp
import random


# 可以使用 
# SKP20 （主动发）,激光雷达,串口转U口
# modbus TCP 协议
# [[int(data_mi_shu1,16),i + 1,i]]，距离，报警，角度
#主采集程序
def SKP20() :
    i=1
    ser_ID=0
    data_mi_Mess=0

    while (int(ser_ID) == 0) :
        ser_ID=int(input("1、U口；2、扩展串口"))
        if ser_ID==1 :
            ser_Name="/dev/ttyUSB0"
        if ser_ID==2 :
            ser_Name="/dev/ttySC0"
        if ser_ID>2 :
            ser_ID = 0
            print (ser_ID)

    LOGGER = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")
    SERVER = modbus_tcp.TcpServer(address="192.168.2.200", port=10020)
    LOGGER.info("running...")
    LOGGER.info("enter 'quit' for closing the server")
# 服务启动
    SERVER.start()
# 建立第一个从机
    SLAVE1 = SERVER.add_slave(1)
    SLAVE1.add_block('A', cst.HOLDING_REGISTERS, 0, 4)  # 地址0，长度1

    ser_mi = serial.Serial(ser_Name, 115200, 8,"N",stopbits=1)

    try:
        while (1): 
            i=i+1
            time.sleep(0.01)
            count=ser_mi.inWaiting()
# 数据的接收
            if count>0:
                time.sleep(0.01)
                serd = ser_mi.inWaiting()
                time.sleep(0.05)
                data_mi=ser_mi.read(serd).hex()

                if data_mi[0:4]=='5507':
                    data_mi_shu1=data_mi[8:12]
                    data_mi_shu2=int(data_mi_shu1,16)/1000

                    print (data_mi_shu2,"米")
                    print (i,"i")
                    data_a=int(data_mi_shu2*100//1)

                    if data_mi_shu2<=0.5:
                        data_mi_Mess=1
                    SLAVE1.set_values('A', 0, [int(data_mi_shu1,16),data_mi_Mess,i])
                    data_mi_Mess=0        
    except KeyboardInterrupt:
        print("\nApplication exit!")
        SERVER.stop()
        ser_mi.close()
        sys.exit(0)

#舵机正位设置
def MotorStupe() :
    none=True
    #使用树莓派板载串口
    Motor_ser = serial.Serial("/dev/ttyAMA0",9600,timeout=1)
    time.sleep(0.1)
    Motor_ser.close
    Motor_ser.open
    while none :
        print("激光雷达启动扫描角度设置：")
        Motor_ID=int(input("1、中心位置；2、起始位置；3、扫描测试 ;4、退出：\n"))
        if Motor_ID==1 :
            command = [0xFF,0x09,0x01,0x02,0x00]
            Motor_ser.write(command)
            Motor_ser.flush()
            Motor_ser.flushInput()
        if  Motor_ID==2 :
            command = [0xFF,0x09,0x01,0x00,0x00]
            Motor_ser.write(command)
            Motor_ser.flush()
            Motor_ser.flushInput()
        if  Motor_ID==3 :
            command = [0xFF,0x09,0x01,0x03,0x00]
            Motor_ser.write(command)
            Motor_ser.flush()
            Motor_ser.flushInput()
            time.sleep(10)
        if  Motor_ID==4 :
            none=False
            Motor_ser.close

if __name__ == '__main__':
    MotorStupe()
    SKP20() 
#    SERVER.stop()
#    ser_mi.close()
    sys.exit(0)