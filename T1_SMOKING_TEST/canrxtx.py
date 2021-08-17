# Description : 收发can报文
# Author : Zengzeng.Duan
# Editor :
# Revision History
# Version       Data         Initials          Description
#  V1.0       20210810      Zengzeng.Duan        Original
#  V1.1       20210818      Yida.Wang       使用logger_smt记录log 
import can
import time
from GAC_TEST_COMMEN_MODULE.external_device import *
from GAC_TEST_COMMEN_MODULE.massage_simulation import *
from GAC_TEST_COMMEN_MODULE.gac_test_uds import *


def send_one(arbitration_id, data):
    msg = can.Message(arbitration_id=arbitration_id,
                      data=data,
                      is_extended_id=False)
    try:
        bus0.send(msg)
        # print("Message sent on {}".format(bus0.channel_info))
    except can.CanError:
        print("Message NOT sent")


def recv():
    msg = bus0.recv(timeout=1)
    try:
        # bus0.send(msg)
        # print(msg)
        # print(msg.timestamp)
        # print(hex(msg.data[0]))  # 接收回来的第一个字节的数据
        # print(hex(msg.arbitration_id))   # 接收回来的ID
        return msg
    except can.CanError:
        print("Message NOT sent")


def CANClear():
    # 清除CAN卡缓存
    bus0.flush_tx_buffer()
    CANRead1000()


def CANRead1000():
    '''读一秒报文'''
    time_start = time.time()
    while True:
        msg = recv()
        if time.time() - time_start > 1:
            break


def CANPeriod():
    '''计算工作模式下报文周期
        返回：1——正常；0——异常'''
    pc.power_on()
    pc.voltage_set_12()
    CANClear()
    rc.ign_on()
    time_cannm_test_start = time.time()
    time_list_3c7 = []
    time_list_387 = []
    time_list_522 = []

    while True:
        msg = recv()
        # print(msg)
        canID = hex(msg.arbitration_id)
        canTimestamp = msg.timestamp

        if canID == "0x387":
            time_list_387.append(canTimestamp)
        elif canID == "0x3c7":
            time_list_3c7.append(canTimestamp)
        elif canID == "0x522":
            time_list_522.append(canTimestamp)

        time_cannm_test_stop = time.time()
        if time_cannm_test_stop - time_cannm_test_start > 5:
            break

    sumtime = 0
    len_3c7 = len(time_list_3c7)
    if len_3c7 > 0:
        logger_smt.info('Pass! Can-message contains 0x3c7')
    else:
        logger_smt.info('Fail! Can-message doesn\'t contains 0x3c7')
        return 0
    for i in range(len_3c7-1):
        intervals = time_list_3c7[i+1] - time_list_3c7[i]
        sumtime += intervals
    period_3c7 = sumtime / (len_3c7-1)
    if period_3c7/1000 > 180 and period_3c7/1000 < 220:
        logger_smt.info('Pass! period of can massage 0x3c7: %.1fms' % float(period_3c7/1000))
    else:
        return 0

    sumtime = 0
    len_387 = len(time_list_387)
    if len_387 > 0:
        logger_smt.info('Pass! Can-message contains 0x387')
    else:
        logger_smt.info('Fail! Can-message doesn\'t contains 0x387')
        return 0
    for i in range(len_387-1):
        intervals = time_list_387[i+1] - time_list_387[i]
        sumtime += intervals
    period_387 = sumtime / (len_387-1)
    if period_387/1000 > 180 and period_387/1000 < 220:
        logger_smt.info('Pass! period of can massage 0x387: %.1fms' % float(period_387/1000))
    else:
        return 0

    sumtime = 0
    len_522 = len(time_list_522)
    if len_522 > 0:
        logger_smt.info('Pass! Can-message contains 0x522')
    else:
        logger_smt.info('Fail! Can-message doesn\'t contains 0x522')
        return 0
    for i in range(len_522-1):
        intervals = time_list_522[i+1] - time_list_522[i]
        sumtime += intervals
    period_522 = sumtime / (len_522-1)
    if period_522/1000 > 180 and period_522/1000 < 220:
        logger_smt.info('Pass! period of can massage 0x522: %.1fms' % float(period_522/1000))
    else:
        return 0
    
    return 1


def PeriodIGNOff():
    '''IGN_Off情况下发送0x510,计算报文周期
        返回：1——正常；0——异常'''
    pc.power_on()
    pc.voltage_set_12()
    rc.ign_on()
    time.sleep(5)
    rc.ign_off()
    CANClear()
    
    time_cannm_test_start = time.time()
    thr_510.start()
    time_list_3c7 = []
    time_list_387 = []
    time_list_522 = []
    while True:
        msg = bus0.recv()
        canID = hex(msg.arbitration_id)
        canTimestamp = msg.timestamp
        if canID == "0x387":
            time_list_387.append(canTimestamp)
        elif canID == "0x3c7":
            time_list_3c7.append(canTimestamp)
        elif canID == "0x522":
            time_list_522.append(canTimestamp)
        time_cannm_test_stop = time.time()
        if time_cannm_test_stop - time_cannm_test_start > 5:
            thr_510.stop()
            break

    sumtime = 0
    len_3c7 = len(time_list_3c7)
    for i in range(len_3c7-1):
        intervals = time_list_3c7[i+1] - time_list_3c7[i]
        sumtime += intervals
    period_3c7 = sumtime / (len_3c7-1)
    if period_3c7/1000 > 180 and period_3c7/1000 < 220:
        logger_smt.info('Pass! period of can massage 0x3c7: %.1fms' % float(period_3c7/1000))
    else:
        return 0

    sumtime = 0
    len_387 = len(time_list_387)
    for i in range(len_387-1):
        intervals = time_list_387[i+1] - time_list_387[i]
        sumtime += intervals
    period_387 = sumtime / (len_387-1)
    if period_387/1000 > 180 and period_387/1000 < 220:
        logger_smt.info('Pass! period of can massage 0x387: %.1fms' % float(period_387/1000))
    else:
        return 0

    sumtime = 0
    len_522 = len(time_list_522)
    if len_522 == 5:
        logger_smt.info('Pass! CanNM 0x522 sends five frames')
    else:
        logger_smt.info('Fail! CanNM 0x522 sends more or less than five frames')
        return 0
    for i in range(len_522-1):
        intervals = time_list_522[i+1] - time_list_522[i]
        sumtime += intervals
    period_522 = sumtime / (len_522-1)
    if period_522/1000 > 180 and period_522/1000 < 220:
        logger_smt.info('Pass! period of can massage 0x522: %.1fms' % float(period_522/1000))
    else:
        return 0
    
    return 1
