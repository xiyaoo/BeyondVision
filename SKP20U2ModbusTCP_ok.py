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

i=1
# 可以使用 
# SKP20 （主动发）,激光雷达,串口转U口
# modbus TCP 协议
# [[int(data_mi_shu1,16),i + 1,i]]，距离，报警，角度
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
    
SERVER.stop()