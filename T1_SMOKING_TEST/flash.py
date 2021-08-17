# Description : SPI刷写测试及CAN刷写测试
# Author : Zengzeng.Duan
# Editor :
# Revision History
# Version       Data         Initials          Description
#  V1.0       20210810      Zengzeng.Duan        Original
#  V1.1       20210818      Yida.Wang          1. 使用logger_smt记录log 
#                                              2. 将使用的bin文件全路径设定为宏定义，存于gac_define
from operator import length_hint
import math
import numpy as np
import struct
import time
from GAC_TEST_COMMEN_MODULE.external_device import *
from GAC_TEST_COMMEN_MODULE.gac_test_uds import *
from GAC_TEST_COMMEN_MODULE.massage_simulation import *


def SecureAlgo(seed, level):
    '''根据种子计算密钥的函数'''
    if level == 1:  # App unlock level
        constant = np.uint32(0xE8D59AC7)
    elif level == 17:  # BT unlock level
        constant = np.uint32(0x6EB5FCA0)
    else:
        print("Unkown unlock level")
    result = np.uint32(0)
    upack = struct.unpack('>L', seed)[0]
    u32seed = np.uint32(upack)
    rightshift = np.uint32(u32seed >> 9)
    leftshift = np.uint32(u32seed << 22)
    result = rightshift | leftshift
    result = np.uint32(result)
    result *= 6
    result = np.uint32(result)
    result ^= constant
    result = np.uint32(result)
    leftshift = np.uint32(result << 14)
    rightshift = np.uint32(result >> 17)
    result = leftshift | rightshift
    result = np.uint32(result)
    return struct.pack('>L', result)

def VerBack(SwVerison_comp):
    '''CAN刷写
        返回：1——正常；0——异常'''
    pc.voltage_set_12()
    time.sleep(1)
    pc.power_on()
    rc.ign_on()
    time.sleep(1)
    logger_smt.info('CANFlash-test')

    with uds_client().client_connect() as client:
        client.change_session(3)  # 进入拓展会话
        try:
            write_data = client.write_data_by_identifier(did=0x0110, value=0xff)
            print('已将0110写为ff')
        except:
            print('没有将0110写为ff')

        # 流程校验2  $22 读DID0110
        try:
            read_data = client.read_data_by_identifier(0x0110)
            if read_data.data.hex() == '0110ff':
                print('Pass! 2  回复肯定响应 62 01 10 FF')  # 回复肯定响应
            else:
                print('Fail! 2  回复肯定响应,但不返回 62 01 10 ')
        except:
            print('Fail! 2  回复否定响应')

        # 流程校验3  $10 切换回话模式；03表示进入拓展会话
        client.change_session(3)
        # thr_3e80.restart()
        try:
            change_session = client.change_session(3)
            # print(change_session.data.hex())        #正响应:50  自服务:03   P2 Sever_max:0032   P2* Sever_max:00c8
            if change_session.data.hex() == '03003200c8':
                print('Pass! 3  回复肯定响应 50 03 00 32 00 c8')
            else:
                print('Fail! 3  回复否定响应，但不返回 50 03 00 32 00 c8')
        except:
            print('Fail! 3  回复否定响应')
        # 流程校验4  $31 开启例程；01表示开启例程、0203表示刷新条件
        try:
            routine_control = client.routine_control(
                routine_id=0x0203, control_type=0x01, data=None)
            if routine_control.data.hex() == '010203':
                print('Pass! 4  回复肯定响应 71 01 02 03')
            else:
                print('Fail! 4  回复肯定响应，但不返回 71 01 02 03')
        except:
            print('Fail! 4  回复否定响应')

        # 流程校验5  $85 控制DTC存储；02表示关闭DTC存储
        try:
            control_dtc_setting = client.control_dtc_setting(
                setting_type=0x02, data=None)
            if control_dtc_setting.data.hex() == '02':
                print('Pass! 5  回复肯定响应 C5 02')
            else:
                print('Fail! 5  回复肯定响应，但不返回 C5 02')
        except:
            print('Fail! 5  回复否定响应')

        # 流程校验6  $28 控制诊断通信；03表示关闭收发通信
        try:
            communication_control = client.communication_control(
                control_type=0x03, communication_type=0x01)
            # print(communication_control.data.hex())
            if communication_control.data.hex() == '03':
                print('Pass! 6  回复肯定响应 68 03')
            else:
                print('Fail! 6  回复肯定响应，但不返回 68 03')
        except:
            print('Fail! 6  回复否定响应')

        # 流程校验7  $10 切换会话模式；02表示进入编程会话
        client.change_session(2)
        change_session = client.change_session(2)
        # print(change_session.data.hex())    #同3
        try:
            if change_session.data.hex() == '02003200c8':
                print('Pass! 7  回复肯定响应 50 02 00 32 00 c8')
            else:
                print('Fail! 7  回复肯定响应，但不返回 50 02 00 32 00 c8')
        except:
            print('Fail! 7  回复否定响应')

        # 流程校验8  $27 客户端向服务器请求种子
        try:
            request_seed = client.request_seed(level=0x11)  # for reprogramming
            # print(request_seed.data.hex()[ :2])                        #可视化seed
            if request_seed.data.hex()[:2] == '11':
                print('Pass! 8  回复肯定响应 67 11 seed')
            else:
                print('Fail! 8  回复肯定响应,但不返回 67 11 seed')
        except:
            print('Fail! 8  回复否定响应')

        # 流程校验9  $27 客户端向服务端发送种子
        try:
            send_key = client.send_key(level=18, key=SecureAlgo(
                seed=request_seed.service_data.seed, level=17))
            if send_key.data.hex() == '12':
                print('Pass! 9  回复肯定响应 67 12')
            else:
                print('Fail! 9  回复肯定响应，但不返回 67 12')
        except:
            print('Fail! 9  回复否定响应')

        # 流程校验10 $2E 写服务
        try:

            # value=11 21 07 30 FF FFFF FF        gongjuid：0x11 年、月、日、：0x210730  工具序列号：0xFFFFFFFF
            write_data = client.write_data_by_identifier(did=0xF184, value=0x11)
            # print(write_data.data.hex())
            if write_data.data.hex() == 'f184':
                print('Pass! 10 回复肯定响应 F1 84')
            else:
                print('Fail! 10 回复肯定响应，但不返回 F1 84')
        except:
            print('Fail! 10 回复否定响应')

        # 流程校验11 $34 请求下载数据
        from udsoncan import MemoryLocation
        with open(PATH_FLS, 'rb') as f:
            # 在bytes转为了int型中，会转换16进制（int）运算
            f.seek(1, 0)  # 将文件指针从文件开头，向后移动到 1 个字符的位置
            s1 = f.read(4)  # 读取个4字节，文件指针自动后移4个数据
            add = int.from_bytes(s1, byteorder='big', signed=False)
            f.seek(5, 0)
            s2 = f.read(4)
            mer = int.from_bytes(s2, byteorder='big', signed=False)
            # print(add,mer)
        try:
            memorylocation = MemoryLocation(
                address=add, memorysize=mer, address_format=32, memorysize_format=32)
            #memorylocation = MemoryLocation(address = 0x1FFFF000, memorysize = 0x000001F8, address_format=32, memorysize_format=32)
            request_download = client.request_download(
                memory_location=memorylocation)
            # print(request_download.data.hex())
            if request_download.data.hex() == '200402':
                print('Pass! 11 回复肯定响应 74 20 04 02')
            else:
                print('Fail! 11 回复肯定响应，但不返回 74 20 04 02')
        except:
            print('Fail! 11 回复否定响应')

        # 流程校验12 $36 发送数据
        with open(PATH_FLS, 'rb') as f:
            f.seek(9, 0)
            s1 = f.read()
        try:
            # 获取sequence_number，需要看一下log文件
            transfer_data = client.transfer_data(sequence_number=0x01, data=s1)
            if transfer_data.data.hex() == '01':
                print('Pass! 12 回复肯定响应 76 01')
            else:
                print('Fail! 12 回复肯定响应，但不返回 76 01')
        except:
            print('Fail! 12 回复否定响应')

        # 流程校验13 $37 退出数据传输
        try:
            client.request_transfer_exit()
            print('Pass! 13 回复肯定响应')
        except:
            print('Fail! 13 回复否定响应')

        # 流程校验14 $31 控制ECU例程；01开启例程、0202表示核对CRC效验；
        # FlashDriver效验码固定，无法获取；APP可从bin文件中获取
        s1 = b"\x8C\x70\x8B\x3C"
        try:
            routine_control = client.routine_control(
                routine_id=0x0202, control_type=0x01, data=s1)
            # print(routine_control.data.hex())
            if routine_control.data.hex() == '01020200':  # 文档要求回复01020200
                print('Pass! 14 回复肯定响应 71 01 02 02 00')
            else:
                print('Fail! 14 回复肯定响应，但不返回71 01 02 02 00')
        except:
            print('Fail! 14 回复否定响应')
        # 流程校验15 $31 FFOO表示擦除内存、44表示格式标识符，后接8个字节--地址4个，内存长度4个
        with open(PATH_APP_T, 'rb') as f:
            # 在bytes转为了int型中，会转换16进制（int）运算
            f.seek(33, 0)
            s1 = f.read(8)
            s2 = b'\x44' + s1
        try:
            # log看像地址和数据
            read_data15 = client.routine_control(
                routine_id=0xFF00, control_type=0x01, data=s2)
            # print(read_data15.data.hex())
            if read_data15.data.hex() == '01ff0000':
                print('Pass! 15 回复肯定响应 71 01 FF 00 00')
            else:
                print('Fail! 15 回复肯定响应，但不返回 71 01 FF 00 00')
        except:
            print('Fail! 15 回复否定响应')

        # 流程校验16 $34
        with open(PATH_APP_T, 'rb') as f:
            # 在bytes转为了int型中，会转换16进制（int）运算
            f.seek(33, 0)
            s1 = f.read(4)
            add = int.from_bytes(s1, byteorder='big', signed=False)
            f.seek(37, 0)
            s2 = f.read(4)
            mer = int.from_bytes(s2, byteorder='big', signed=False)
            memorylocation = MemoryLocation(
                address=add, memorysize=mer, address_format=32, memorysize_format=32)
        try:
            request_download = client.request_download(
                memory_location=memorylocation)
            if request_download.data.hex() == '200402':
                print('Pass! 16 回复肯定响应 74 20 04 02')
            else:
                print('Fail! 16 回复肯定响应，但不返回 74 20 04 02')
        except:
            print('Fail! 16 回复否定响应')

        # 流程校验17 $36 需要传输多少个帧数据
        try:
            with open(PATH_APP_T, 'rb') as f:
                f.seek(41, 0)
                data_len = length_hint(f.read())
                len_fre = data_len / 1024
                len = math.ceil(len_fre)
                for i in range(len):
                    a = 41 + i * 1024
                    f.seek(a, 0)
                    data = f.read(1024)
                    val_h = i + 1
                    if i < 16:
                        val = '0x{:02X}'.format(val_h)
                    else:
                        val = hex(val_h)
                    val = int(val, 16)
                    # print(val)
                    transfer_data = client.transfer_data(
                        sequence_number=val, data=data)
            print('Pass! 17 回复肯定响应 76')

        except:
            print('Fail! 17 回复否定响应')

        # 流程校验18
        try:
            client.request_transfer_exit()
            print('Pass! 18 回复肯定响应')
        except:
            print('Fail! 18 回复否定响应')

        # 流程校验20 $31
        with open(PATH_APP_T, 'rb') as f:
            # 在bytes转为了int型中，会转换16进制（int）运算
            f.seek(28, 0)
            s1 = f.read(4)
        try:
            routine_control = client.routine_control(
                routine_id=0x0202, control_type=0x01, data=s1)
            # print(routine_control.data.hex())
            if routine_control.data.hex() == '01020200':  # 文档要求回复01020200
                print('Pass! 20 回复肯定响应 71 01 02 02 00')
            else:
                print('Fail! 20 回复肯定响应，但不返回 71 01 02 02 00')
        except:
            print('Fail! 20 回复否定响应')

        # 流程校验22 $31
        try:
            routine_control = client.routine_control(
                routine_id=0xFF01, control_type=0x01)
            if routine_control.data.hex() == '01ff0100':
                print('Pass! 22 回复肯定响应 71 01 FF 01 00')
            else:
                print('Fail! 22 回复肯定响应，但不返回 71 01 FF 01 00')
        except:
            print('Fail! 22 回复否定响应')

        # 流程校验23 $2E 日期
        try:
            write_data = client.write_data_by_identifier(
                did=0xF199, value=1)  # 这里的value为一个任意值，子函数中不会调用
            if write_data.data.hex() == 'f199':
                print('Pass! 23 回复肯定响应 6E F1 99')
            else:
                print('Fail! 23 回复肯定响应，但不返回 6E F1 99')
        except:
            print('Fail! 23 回复否定响应')

        # 流程校验24 $11 ECU复位；01表示硬件复位
        try:
            ecu_reset = client.ecu_reset(reset_type=0x01)
            if ecu_reset.data.hex() == '01':
                print('Pass! 24 回复肯定响应 51 01')
            else:
                print('Fail! 24 回复肯定响应，但内容不为 51 01')
        except:
            print('Fail! 24 回复否定响应')

        # 输出软件版本
        SwVerison = client.read_data_by_identifier(0xf189).service_data.values[0xf189]
        print(SwVerison)
        if SwVerison_comp == SwVerison:
            logger_smt.info('Pass! Test engineering backtracking is ok')
            return 1
        else:
            logger_smt.info('Fail! Test engineering backtracking is not ok')
            return 0

def CANFlash():
    '''CAN刷写返回：1——正常；0——异常'''
    pc.voltage_set_12()
    time.sleep(1)
    pc.power_on()
    rc.ign_on()
    time.sleep(1)
    logger_smt.info('CANFlash-test')
    with uds_client().client_connect() as client:
        client.change_session(3)  # 进入拓展会话
        SwVerison_comp = client.read_data_by_identifier(0xf189).service_data.values[0xf189]
        try:
            write_data = client.write_data_by_identifier(did=0x0110, value=0xff)
            print('已将0110写为ff')
        except:
            print('没有将0110写为ff')

        # 流程校验2  $22 读DID0110
        try:
            read_data = client.read_data_by_identifier(0x0110)
            if read_data.data.hex() == '0110ff':
                print('Pass! 2  回复肯定响应 62 01 10 FF')  # 回复肯定响应
            else:
                print('Fail! 2  回复肯定响应,但不返回 62 01 10 ')
        except:
            print('Fail! 2  回复否定响应')

        # 流程校验3  $10 切换回话模式；03表示进入拓展会话
        client.change_session(3)
        # thr_3e80.restart()
        try:
            change_session = client.change_session(3)
            # print(change_session.data.hex())        #正响应:50  自服务:03   P2 Sever_max:0032   P2* Sever_max:00c8
            if change_session.data.hex() == '03003200c8':
                print('Pass! 3  回复肯定响应 50 03 00 32 00 c8')
            else:
                print('Fail! 3  回复否定响应，但不返回 50 03 00 32 00 c8')
        except:
            print('Fail! 3  回复否定响应')
        # 流程校验4  $31 开启例程；01表示开启例程、0203表示刷新条件
        try:
            routine_control = client.routine_control(
                routine_id=0x0203, control_type=0x01, data=None)
            if routine_control.data.hex() == '010203':
                print('Pass! 4  回复肯定响应 71 01 02 03')
            else:
                print('Fail! 4  回复肯定响应，但不返回 71 01 02 03')
        except:
            print('Fail! 4  回复否定响应')

        # 流程校验5  $85 控制DTC存储；02表示关闭DTC存储
        try:
            control_dtc_setting = client.control_dtc_setting(
                setting_type=0x02, data=None)
            if control_dtc_setting.data.hex() == '02':
                print('Pass! 5  回复肯定响应 C5 02')
            else:
                print('Fail! 5  回复肯定响应，但不返回 C5 02')
        except:
            print('Fail! 5  回复否定响应')

        # 流程校验6  $28 控制诊断通信；03表示关闭收发通信
        try:
            communication_control = client.communication_control(
                control_type=0x03, communication_type=0x01)
            # print(communication_control.data.hex())
            if communication_control.data.hex() == '03':
                print('Pass! 6  回复肯定响应 68 03')
            else:
                print('Fail! 6  回复肯定响应，但不返回 68 03')
        except:
            print('Fail! 6  回复否定响应')

        # 流程校验7  $10 切换会话模式；02表示进入编程会话
        client.change_session(2)
        change_session = client.change_session(2)
        # print(change_session.data.hex())    #同3
        try:
            if change_session.data.hex() == '02003200c8':
                print('Pass! 7  回复肯定响应 50 02 00 32 00 c8')
            else:
                print('Fail! 7  回复肯定响应，但不返回 50 02 00 32 00 c8')
        except:
            print('Fail! 7  回复否定响应')

        # 流程校验8  $27 客户端向服务器请求种子
        try:
            request_seed = client.request_seed(level=0x11)  # for reprogramming
            # print(request_seed.data.hex()[ :2])                        #可视化seed
            if request_seed.data.hex()[:2] == '11':
                print('Pass! 8  回复肯定响应 67 11 seed')
            else:
                print('Fail! 8  回复肯定响应,但不返回 67 11 seed')
        except:
            print('Fail! 8  回复否定响应')

        # 流程校验9  $27 客户端向服务端发送种子
        try:
            send_key = client.send_key(level=18, key=SecureAlgo(
                seed=request_seed.service_data.seed, level=17))
            if send_key.data.hex() == '12':
                print('Pass! 9  回复肯定响应 67 12')
            else:
                print('Fail! 9  回复肯定响应，但不返回 67 12')
        except:
            print('Fail! 9  回复否定响应')

        # 流程校验10 $2E 写服务
        try:
            # value=11 21 07 30 FF FFFF FF        gongjuid：0x11 年、月、日、：0x210730  工具序列号：0xFFFFFFFF
            write_data = client.write_data_by_identifier(did=0xF184, value=0x11)
            # print(write_data.data.hex())
            if write_data.data.hex() == 'f184':
                print('Pass! 10 回复肯定响应 F1 84')
            else:
                print('Fail! 10 回复肯定响应，但不返回 F1 84')
        except:
            print('Fail! 10 回复否定响应')

        # 流程校验11 $34 请求下载数据
        from udsoncan import MemoryLocation
        with open(PATH_FLS, 'rb') as f:
            # 在bytes转为了int型中，会转换16进制（int）运算
            f.seek(1, 0)  # 将文件指针从文件开头，向后移动到 1 个字符的位置
            s1 = f.read(4)  # 读取个4字节，文件指针自动后移4个数据
            add = int.from_bytes(s1, byteorder='big', signed=False)
            f.seek(5, 0)
            s2 = f.read(4)
            mer = int.from_bytes(s2, byteorder='big', signed=False)
            # print(add,mer)
        try:
            memorylocation = MemoryLocation(
                address=add, memorysize=mer, address_format=32, memorysize_format=32)
            #memorylocation = MemoryLocation(address = 0x1FFFF000, memorysize = 0x000001F8, address_format=32, memorysize_format=32)
            request_download = client.request_download(
                memory_location=memorylocation)
            # print(request_download.data.hex())
            if request_download.data.hex() == '200402':
                print('Pass! 11 回复肯定响应 74 20 04 02')
            else:
                print('Fail! 11 回复肯定响应，但不返回 74 20 04 02')
        except:
            print('Fail! 11 回复否定响应')

        # 流程校验12 $36 发送数据
        with open(PATH_FLS, 'rb') as f:
            f.seek(9, 0)
            s1 = f.read()
        try:
            # 获取sequence_number，需要看一下log文件
            transfer_data = client.transfer_data(sequence_number=0x01, data=s1)
            if transfer_data.data.hex() == '01':
                print('Pass! 12 回复肯定响应 76 01')
            else:
                print('Fail! 12 回复肯定响应，但不返回 76 01')
        except:
            print('Fail! 12 回复否定响应')

        # 流程校验13 $37 退出数据传输
        try:
            client.request_transfer_exit()
            print('Pass! 13 回复肯定响应')
        except:
            print('Fail! 13 回复否定响应')

        # 流程校验14 $31 控制ECU例程；01开启例程、0202表示核对CRC效验；
        # FlashDriver效验码固定，无法获取；APP可从bin文件中获取
        s1 = b"\x8C\x70\x8B\x3C"
        try:
            routine_control = client.routine_control(
                routine_id=0x0202, control_type=0x01, data=s1)
            # print(routine_control.data.hex())
            if routine_control.data.hex() == '01020200':  # 文档要求回复01020200
                print('Pass! 14 回复肯定响应 71 01 02 02 00')
            else:
                print('Fail! 14 回复肯定响应，但不返回71 01 02 02 00')
        except:
            print('Fail! 14 回复否定响应')
        # 流程校验15 $31 FFOO表示擦除内存、44表示格式标识符，后接8个字节--地址4个，内存长度4个
        with open(PATH_APP_C, 'rb') as f:
            # 在bytes转为了int型中，会转换16进制（int）运算
            f.seek(33, 0)
            s1 = f.read(8)
            s2 = b'\x44' + s1
        try:
            # log看像地址和数据
            read_data15 = client.routine_control(
                routine_id=0xFF00, control_type=0x01, data=s2)
            # print(read_data15.data.hex())
            if read_data15.data.hex() == '01ff0000':
                print('Pass! 15 回复肯定响应 71 01 FF 00 00')
            else:
                print('Fail! 15 回复肯定响应，但不返回 71 01 FF 00 00')
        except:
            print('Fail! 15 回复否定响应')

        # 流程校验16 $34
        with open(PATH_APP_C, 'rb') as f:
            # 在bytes转为了int型中，会转换16进制（int）运算
            f.seek(33, 0)
            s1 = f.read(4)
            add = int.from_bytes(s1, byteorder='big', signed=False)
            f.seek(37, 0)
            s2 = f.read(4)
            mer = int.from_bytes(s2, byteorder='big', signed=False)
            memorylocation = MemoryLocation(
                address=add, memorysize=mer, address_format=32, memorysize_format=32)
        try:
            request_download = client.request_download(
                memory_location=memorylocation)
            if request_download.data.hex() == '200402':
                print('Pass! 16 回复肯定响应 74 20 04 02')
            else:
                print('Fail! 16 回复肯定响应，但不返回 74 20 04 02')
        except:
            print('Fail! 16 回复否定响应')

        try:
            with open(PATH_APP_C, 'rb') as f:
                f.seek(41, 0)
                data_len = length_hint(f.read())
                len_fre = data_len / 1024
                len = math.ceil(len_fre)
                for i in range(len):
                    a = 41 + i * 1024
                    f.seek(a, 0)
                    data = f.read(1024)
                    val_h = i + 1
                    if i < 16:
                        val = '0x{:02X}'.format(val_h)
                    else:
                        val = hex(val_h)
                    val = int(val, 16)
                    # print(val)
                    transfer_data = client.transfer_data(
                        sequence_number=val, data=data)
            print('Pass! 17 回复肯定响应 76')

        except:
            print('Fail! 17 回复否定响应')

        # 流程校验18
        try:
            client.request_transfer_exit()
            print('Pass! 18 回复肯定响应')
        except:
            print('Fail! 18 回复否定响应')

        # 流程校验20 $31
        with open(PATH_APP_C, 'rb') as f:
            # 在bytes转为了int型中，会转换16进制（int）运算
            f.seek(28, 0)
            s1 = f.read(4)
        try:
            routine_control = client.routine_control(
                routine_id=0x0202, control_type=0x01, data=s1)
            # print(routine_control.data.hex())
            if routine_control.data.hex() == '01020200':  # 文档要求回复01020200
                print('Pass! 20 回复肯定响应 71 01 02 02 00')
            else:
                print('Fail! 20 回复肯定响应，但不返回 71 01 02 02 00')
        except:
            print('Fail! 20 回复否定响应')

        # 流程校验22 $31
        try:
            routine_control = client.routine_control(
                routine_id=0xFF01, control_type=0x01)
            if routine_control.data.hex() == '01ff0100':
                print('Pass! 22 回复肯定响应 71 01 FF 01 00')
            else:
                print('Fail! 22 回复肯定响应，但不返回 71 01 FF 01 00')
        except:
            print('Fail! 22 回复否定响应')

        # 流程校验23 $2E 日期
        try:
            write_data = client.write_data_by_identifier(
                did=0xF199, value=1)  # 这里的value为一个任意值，子函数中不会调用
            if write_data.data.hex() == 'f199':
                print('Pass! 23 回复肯定响应 6E F1 99')
            else:
                print('Fail! 23 回复肯定响应，但不返回 6E F1 99')
        except:
            print('Fail! 23 回复否定响应')

        # 流程校验24 $11 ECU复位；01表示硬件复位
        try:
            ecu_reset = client.ecu_reset(reset_type=0x01)
            if ecu_reset.data.hex() == '01':
                print('Pass! 24 回复肯定响应 51 01')
            else:
                print('Fail! 24 回复肯定响应，但内容不为 51 01')
        except:
            print('Fail! 24 回复否定响应')
        # 输出软件版本
        SwVerison = client.read_data_by_identifier(
            0xf189).service_data.values[0xf189]
        print(SwVerison)
        if "S.B00" in SwVerison:
            logger_smt.info('Pass! CANFlash is ok')
            # return 1
        else:
            logger_smt.info('Fail! CANFlash is not ok')
            return 0
    verback = VerBack(SwVerison_comp)
    return verback

def SPIFlash():
    '''SPI刷写
        返回：1——正常；0——异常'''
    time.sleep(10)
    pc.power_on()
    pc.voltage_set_12()
    rc.ign_on()
    time.sleep(15)
    with uds_client().client_connect() as client:
        SwVerison_comp = client.read_data_by_identifier(0xf189).service_data.values[0xf189]
    logger_smt.info('SPIFlash-test')
    if Config_list["connection"] == "Serial":
        j2_ser = serial.Serial(Config_list["com_port_j2"], 115200)
        j2_ser.timeout = 0.5
        j2_ser.writeTimeout = 0.5
        j2_ser.write(b'root\n')
        j2_ser.write(b'\n')
        time.sleep(1)
        j2_ser.write(b'root\n')
        j2_ser.write(b'\n')
        time.sleep(1)
        j2_ser.write(b'cd /userdata/transfer\n')
        time.sleep(1)
        j2_ser.write(b'export LD_LIBRARY_PATH=/app/lib:$LD_LIBRARY_PATH\n')
        time.sleep(1)
        j2_ser.write(b'./test_interface 2\n')
        j2_ser.close()
    time.sleep(20)
    while True:
        try:
            uc = uds_client().client_connect()
            with uc as client:
                SwVerison = client.read_data_by_identifier(
                    0xf189).service_data.values[0xf189]
            break
        except:
            pass
    
    if 'S.C00' in SwVerison:
        logger_smt.info('Pass! SPIFlash is ok')
        VerBack(SwVerison_comp)
        return 1
    else:
        logger_smt.info('Fail! SPIFlash is not ok')
        VerBack(SwVerison_comp)
        return 0
    

