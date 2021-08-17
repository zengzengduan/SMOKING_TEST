# Description : 模式转换测试
# Author : Zengzeng.Duan
# Editor : Yida.Wang
# Revision History
# Version       Data         Initials          Description
#  V1.0       20210810      Zengzeng.Duan        Original
#  V1.1       20210818      Yida.Wang          1. 使用logger_smt记录log 
#                                              2. 增加通信模式及低功耗模式电压说明

from GAC_TEST_COMMEN_MODULE.external_device import *
from canrxtx import *

def WorkMode():
    '''测试工作模式是否正常
        返回：1——正常；0——异常'''
    time.sleep(1)
    pc.voltage_set_12()
    pc.power_on()
    CANClear()
    rc.ign_on()
    time.sleep(5)
    starttime = time.time()
    while True:
        if pc.power_meas() > 6:
            break
        if time.time() - starttime > 10:
            break
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() < 6:
        logger_smt.info("Fail! working mode is not OK!!!, end=---")
        if msg == None:
            logger_smt.info('Reason: no can-message in working mode')

        if pc.power_meas() < 6:
            logger_smt.info('Reason: camera does not work in working mode')
        pc.power_off()
        time.sleep(1)
        return 0

    else:
        logger_smt.info("Pass! working mode is OK!")
        pc.power_off()
        time.sleep(1)
        return 1


def ComMode():
    '''测试通信模式是否正常
        返回：1——正常；0——异常'''
    time.sleep(1)
    pc.voltage_set_8()
    pc.power_on()
    CANClear()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() > 6:
        logger_smt.info('Fail! communication mode (8V) is not OK!!!, end=---')
        if msg == None:
            logger_smt.info('Reason: no can-message in communication mode (8V)')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in communication mode (8V)')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! communication mode (8V) is OK!')

    CANClear()
    pc.voltage_set_17()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() > 6:
        logger_smt.info('Fail! communication mode (17V) is not OK!!!, end=---')
        if msg == None:
            logger_smt.info('Reason: no can-message in communication mode (17V)')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in communication mode (17V)')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! communication mode (17V) is OK!')

    pc.power_off()
    time.sleep(1)
    return 1


def LowMode():
    '''测试低功耗模式是否正常
        返回：1——正常；0——异常'''
    time.sleep(1)
    pc.voltage_set_6_5()
    pc.power_on()
    CANClear()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg != None or pc.power_meas() > 6:
        logger_smt.info('Fail! Low power mode (6.5V) is not OK!!!, end=---')
        if msg != None:
            logger_smt.info('Reason: can-message received in low power mode (6.5V)')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in low power mode (6.5V)')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! Low power mode (6.5V) is OK!')

    CANClear()
    pc.voltage_set_18_5()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg != None or pc.power_meas() > 6:
        logger_smt.info('Fail! Low power mode (18.5V) is not OK!!!, end=---')
        if msg != None:
            logger_smt.info('Reason: can-message received in low power mode (18.5V)')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in low power mode (18.5V)')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! Low power mode (18.5V) is OK!')

    pc.power_off()
    time.sleep(1)
    return 1


def WorkToCom():
    '''测试工作模式到通信模式的转换
        返回：1——正常；0——异常'''
    # CANClear()
    time.sleep(1)
    pc.power_on()
    pc.voltage_set_12()
    rc.ign_on()
    time.sleep(5)
    starttime = time.time()
    while True:
        if pc.power_meas() > 6:
            break
        if time.time() - starttime > 10:
            break

    CANClear()
    pc.voltage_set_8()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() > 6:
        logger_smt.info('Fail! working mode to communication mode (12 V to 8 V) start, end=---')
        if msg == None:
            logger_smt.info('Reason: no can-message in communication mode start')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in communication mode start')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! working mode to communication mode (12 V to 8 V)')

    CANClear()
    pc.voltage_set_12()
    rc.ign_on()
    time.sleep(5)
    starttime = time.time()
    while True:
        if pc.power_meas() > 6:
            break
        if time.time() - starttime > 10:
            break

    CANClear()
    pc.voltage_set_17()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() > 6:
        logger_smt.info('Fail! working mode to communication mode (12 V to  V17) start, end=---')
        if msg == None:
            logger_smt.info('Reason: no can-message in communication mode start')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in communication mode start')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! working mode to communication mode (12 V to 17 V)')

    pc.power_off()
    time.sleep(1)
    return 1


def ComToWork():
    '''测试通信模式到工作模式的转换
        返回：1——正常；0——异常'''
    # CANClear()
    time.sleep(1)
    pc.power_on()
    pc.voltage_set_8()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_12()
    rc.ign_on()
    time.sleep(5)
    starttime = time.time()
    while True:
        if pc.power_meas() > 6:
            break
        if time.time() - starttime > 10:
            break
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() < 6:
        logger_smt.info("Fail! communication mode to working mode (8 V to 12 V) during, end=---")
        if msg == None:
            logger_smt.info('Reason: no can-message in working mode')

        if pc.power_meas() < 6:
            logger_smt.info('Reason: camera does not work in working mode')
            pc.power_off()
            time.sleep(1)
            return 0

    else:
        logger_smt.info("Pass! communication mode to working mode (8 V to 12 V)")

    CANClear()
    pc.voltage_set_17()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_12()
    rc.ign_on()
    time.sleep(5)
    starttime = time.time()
    while True:
        if pc.power_meas() > 6:
            break
        if time.time() - starttime > 10:
            break
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() < 6:
        logger_smt.info("Fail! communication mode to working mode (17 V to 12 V) during, end=---")
        if msg == None:
            logger_smt.info('Reason: no can-message in working mode')

        if pc.power_meas() < 6:
            logger_smt.info('Reason: camera does not work in working mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! communication mode to working mode (17 V to 12 V)')

    pc.power_off()
    time.sleep(1)
    return 1


def WorkToLow():
    '''测试工作模式到低功耗模式的转换
        返回：1——正常；0——异常'''
    # CANClear()
    time.sleep(1)
    pc.power_on()
    pc.voltage_set_12()
    rc.ign_on()
    time.sleep(5)
    starttime = time.time()
    while True:
        if pc.power_meas() > 6:
            break
        if time.time() - starttime > 10:
            break

    CANClear()
    pc.voltage_set_6_5()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg != None or pc.power_meas() > 6:
        logger_smt.info('Fail! working mode to low power mode (12 V to 6.5 V) start, end=---')
        if msg != None:
            logger_smt.info('Reason: can-message received in low power mode')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in low power mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! working mode to low power mode (12 V to 6.5 V)')

    CANClear()
    pc.voltage_set_12()
    rc.ign_on()
    time.sleep(5)
    starttime = time.time()
    while True:
        if pc.power_meas() > 6:
            break
        if time.time() - starttime > 10:
            break

    CANClear()
    pc.voltage_set_18_5()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg != None or pc.power_meas() > 6:
        logger_smt.info('Fail! working mode to low power mode (12 V to  V18.5) start, end=---')
        if msg != None:
            logger_smt.info('Reason: can-message received in low power mode')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in low power mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! working mode to low power mode (12 V to 18.5 V)')

    pc.power_off()
    time.sleep(1)
    return 1


def LowToWork():
    '''测试低功耗模式到工作模式的转换
        返回：1——正常；0——异常'''
    # CANClear()
    time.sleep(1)
    pc.power_on()
    pc.voltage_set_6_5()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_12()
    rc.ign_on()
    time.sleep(5)
    starttime = time.time()
    while True:
        if pc.power_meas() > 6:
            break
        if time.time() - starttime > 10:
            break
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() < 6:
        logger_smt.info('Fail! low power mode to working mode (6.5 V to 12 V) start, end=---')
        if msg == None:
            logger_smt.info('Reason: no can-message in working mode')
        if pc.power_meas() < 6:
            logger_smt.info('Reason: camera does not work in working mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! low power mode to working mode (6.5 V to 12 V)')

    CANClear()
    pc.voltage_set_18_5()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_12()
    rc.ign_on()
    time.sleep(5)
    starttime = time.time()
    while True:
        if pc.power_meas() > 6:
            break
        if time.time() - starttime > 10:
            break
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() < 6:
        logger_smt.info('Fail! working mode to communication mode (18.5 V to 12 V) start, end=---')
        if msg == None:
            logger_smt.info('Reason: no can-message in working mode')
        if pc.power_meas() < 6:
            logger_smt.info('Reason: camera does not work in working mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! low power mode to working mode (18.5 V to 12 V)')

    pc.power_off()
    time.sleep(1)
    return 1


def LowToCom():
    '''测试低功耗模式到通信模式的转换
        返回：1——正常；0——异常'''
    # CANClear()
    time.sleep(1)
    pc.power_on()
    pc.voltage_set_6_5()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_8()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() > 6:
        logger_smt.info('Fail! low power mode to communication mode (6.5 V to 8 V) start, end=---')
        if msg == None:
            logger_smt.info('Reason: no can-message in communication mode')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in communication mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! low power mode to communication mode (6.5 V to 8 V)')

    CANClear()
    pc.voltage_set_6_5()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_17()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() > 6:
        logger_smt.info('Fail! working mode to communication mode (6.5 V to 17 V) start, end=---')
        if msg == None:
            logger_smt.info('Reason: no can-message in communication mode')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in communication mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! low power mode to communication mode (6.5 V to 17 V)')

    CANClear()
    pc.voltage_set_18_5()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_8()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() > 6:
        logger_smt.info('Fail! low power mode to communication mode (18.5 V to 8 V) start, end=---')
        if msg == None:
            logger_smt.info('Reason: no can-message in communication mode')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in communication mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! low power mode to communication mode (18.5 V to 8 V)')

    CANClear()
    pc.voltage_set_18_5()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_17()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg == None or pc.power_meas() > 6:
        logger_smt.info('Fail! working mode to communication mode (18.5 V to 17 V) start, end=---')
        if msg == None:
            logger_smt.info('Reason: no can-message in communication mode')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works in communication mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! low power mode to communication mode (18.5 V to 17 V)')

    pc.power_off()
    time.sleep(1)
    return 1


def ComToLow():
    '''测试通信模式到低功耗模式的转换
        返回：1——正常；0——异常'''
    # CANClear()
    time.sleep(1)
    pc.power_on()
    pc.voltage_set_8()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_6_5()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg != None or pc.power_meas() > 6:
        logger_smt.info('Fail! communication mode to low power mode (8 V to 6.5 V) start, end=---')
        if msg != None:
            logger_smt.info('Reason: can-message received in low power mode')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works low power mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! communication mode to low power mode (8 V to 6.5 V)')

    # CANClear()
    pc.voltage_set_8()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_18_5()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg != None or pc.power_meas() > 6:
        logger_smt.info('Fail! communication mode to low power mode (8 V to 18.5 V) start, end=---')
        if msg != None:
            logger_smt.info('Reason: can-message received in low power mode')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works low power mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! communication mode to low power mode (8 V to 18.5 V)')

    # CANClear()
    pc.voltage_set_17()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_6_5()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg != None or pc.power_meas() > 6:
        logger_smt.info('Fail! communication mode to low power mode (17 V to 6.5 V) start, end=---')
        if msg != None:
            logger_smt.info('Reason: can-message received in low power mode')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works low power mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! communication mode to low power mode (17 V to 6.5 V)')

    # CANClear()
    pc.voltage_set_17()
    rc.ign_on()
    time.sleep(1)

    CANClear()
    pc.voltage_set_18_5()
    rc.ign_on()
    CANRead1000()
    msg = recv()
    if msg != None or pc.power_meas() > 6:
        logger_smt.info(
            'Fail! communication mode to low power mode (17 V to 18.5 V) start, end=---')
        if msg != None:
            logger_smt.info('Reason: can-message received in low power mode')
        if pc.power_meas() > 6:
            logger_smt.info('Reason: camera works low power mode')
            pc.power_off()
            time.sleep(1)
            return 0
    else:
        logger_smt.info('Pass! communication mode to low power mode (17 V to 18.5 V)')

    pc.power_off()
    time.sleep(1)
    return 1


def CanToNoneVoltage():
    '''CAN报文消失电压值
        返回：1——正常；0——异常'''
    time.sleep(1)
    pc.power_on()
    pc.voltage_set_12()   
    VolFlag = 1
    time.sleep(1)
    for voltage10 in range(176, 190):
        voltage = voltage10/10
        UpVol = float(voltage)-0.1
        pc.voltage_set(b'%.1f' %voltage)
        CANClear()
        rc.ign_on()
        CANRead1000()
        msg = recv()
        if msg == None:
            logger_smt.info("upper limit of voltage for can message disappeared during voltage-rise: %.1f" %
                  UpVol)
            if UpVol < 18.1 or UpVol > 18.6:
                VolFlag = 0
            break

    pc.power_on()
    pc.voltage_set_12()
    time.sleep(1)
    for voltage10 in range(75, 66, -1):
        voltage = voltage10/10
        LowVol = float(voltage)+0.1
        pc.voltage_set(b'%.1f' %voltage)
        CANClear()
        rc.ign_on()
        CANRead1000()
        msg = recv()
        if msg == None:
            logger_smt.info("lower limit of voltage for can message disappeared during voltage-drop: %.1f" %
                  LowVol)
            if LowVol < 6.7 or LowVol > 7.2:
                VolFlag = 0
            break
    return VolFlag


def NoneToCanVoltage():
    '''CAN报文出现电压值
        返回：1——正常；0——异常'''
    time.sleep(1)
    pc.power_on()
    pc.voltage_set_12()
    VolFlag = 1
    time.sleep(1)
    for voltage10 in range(66, 75):
        voltage = voltage10/10
        LowVol = voltage
        pc.voltage_set(b'%.1f' %voltage)
        CANClear()
        rc.ign_on()
        CANRead1000()
        msg = recv()
        if msg != None:
            logger_smt.info(
                "lower limit of voltage for can message appeared during voltage-rise: %.1f" % LowVol)
            if LowVol < 6.9 or LowVol > 7.4:
                VolFlag = 0
            break

    pc.power_on()
    pc.voltage_set_12()
    time.sleep(1)
    for voltage10 in range(185, 175, -1):
        voltage = voltage10/10
        UpVol = voltage
        pc.voltage_set(b'%.1f' %voltage)
        CANClear()
        rc.ign_on()
        CANRead1000()
        msg = recv()
        if msg != None:
            logger_smt.info(
                "upper limit of voltage for can message appeared during voltage-drop: %.1f" % UpVol)
            if UpVol < 18.0 or UpVol > 18.5:
                VolFlag = 0
            break
    return VolFlag


def CameraToNoneVoltage():
    '''摄像头消失电压值
        返回：1——正常；0——异常'''
    time.sleep(1)
    pc.power_on()
    pc.voltage_set_12()
    rc.ign_on()
    VolFlag = 1
    time.sleep(5)
    starttime = time.time()
    while True:
        if pc.power_meas() > 6:
            break
        if time.time() - starttime > 10:
            break
    for voltage10 in range(96, 85, -1):
        voltage = voltage10/10
        LowVol = float(voltage)+0.1
        pc.voltage_set(b'%.1f' %voltage)
        time.sleep(1)
        if pc.power_meas() < 6:
            logger_smt.info("lower limit of voltage for camera working to None during voltage-drop: %.1f" %
                  LowVol)
            if LowVol < 8.7 or LowVol > 9.5:
                VolFlag = 0
            break

    pc.power_on()
    pc.voltage_set_12()
    rc.ign_on() 
    time.sleep(5)
    starttime = time.time()
    while True:
        if pc.power_meas() > 6:
            break
        if time.time() - starttime > 10:
            break
    for voltage10 in range(155, 170):
        voltage = voltage10/10
        pc.voltage_set(b'%.1f' %voltage)
        UpVol = float(voltage)-0.1
        time.sleep(1)
        if pc.power_meas() < 6:
            logger_smt.info("upper limit of voltage for camera working to None during voltage-rise: %.1f" %
                  UpVol)
            if UpVol < 16.2 or UpVol > 16.7:
                VolFlag = 0
            break
    return VolFlag


def NoneToCameraVoltage():
    '''摄像头出像电压值
        返回：1——正常；0——异常'''
    time.sleep(1)
    pc.power_on()
    rc.ign_on()
    VolFlag = 1
    time.sleep(1)
    for voltage10 in range(87, 95):
        voltage = voltage10/10
        LowVol = voltage
        pc.voltage_set(b'%.1f' %voltage)
        time.sleep(6)

        if pc.power_meas() > 6:
            logger_smt.info(
                "lower limit of voltage for None to camera working during voltage-rise: %.1f" % LowVol)
            if LowVol < 8.8 or LowVol > 9.3:
                VolFlag = 0
            break

    pc.power_on()
    rc.ign_on()
    time.sleep(1)
    for voltage10 in range(164, 155, -1):
        voltage = voltage10/10
        UpVol = voltage
        pc.voltage_set(b'%.1f' %voltage)
        time.sleep(6)

        if pc.power_meas() > 6:
            logger_smt.info(
                "upper limit of voltage for None to camera working  during voltage-drop: %.1f" % voltage)
            if UpVol < 15.8 or UpVol > 16.3:
                VolFlag = 0
            break
    
    pc.voltage_set_12()
    time.sleep(1)
    pc.power_off()
    time.sleep(1)
    return VolFlag
