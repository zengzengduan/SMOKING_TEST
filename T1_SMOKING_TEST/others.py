# Description : IGN、休眠电流、time.sh
# Author : Zengzeng.Duan
# Editor : Yida.Wang
# Revision History
# Version       Data         Initials          Description
#  V1.0       20210810      Zengzeng.Duan        Original
#  V1.1       20210818      Yida.Wang         1. 测试休眠电流前关闭375，35a，2dc等报文发送 
#                                             2. 使用logger_smt记录log
import paramiko
from contextlib import suppress
from GAC_TEST_COMMEN_MODULE.external_device import *
from canrxtx import *

def IGN():
    '''判断IGN是否正常
        返回：1——正常；0——异常'''
    pc.power_on()
    pc.voltage_set_12()
    time.sleep(0.1)
    rc.ign_off()
    CANClear()
    msg = recv()
    if msg == None:
        time.sleep(1)
        rc.ign_on()
        time.sleep(0.5)
        msg = recv()
        if msg != None:
            logger_smt.info('Pass! IGN work')
            return 1
        else:
            logger_smt.info('Fail! Reason: IGN ON, CAN Massage not received')
            return 0
    else:
        logger_smt.info('Fail! Reason: IGN ON, CAN Massage not received')
        return 0

def ADASL3(ECUName):
    '''判断不同车型的ADASL3功能是否正常
        返回：1——正常；0——异常'''
    pc.power_on()
    pc.voltage_set_12()
    time.sleep(0.1)
    CANClear()
    rc.ign_on()
    time.sleep(1)

    while True:
        msg = recv()
        canID = hex(msg.arbitration_id)
        if canID == "0x3c7":
            msg3 = msg.data[3]
            msg4 = msg.data[4]
            if ECUName == "GAC_A20" or ECUName == "GAC_A29":
                if msg3 == 0x00 and msg4 < 0x10:
                    logger_smt.info('Pass! ADASL3 function is OK!---%s' %ECUName)
                    return 1
                else:
                    logger_smt.info('Fail! ADASL3 function is not OK!!!---%s' %ECUName)
                    return 0
            elif ECUName == "GAC_A13" or ECUName == "GAC_A18":
                if msg3 != 0x00 and msg4 > 0x10:
                    logger_smt.info('Pass! ADASL3 function is OK!---%s' %ECUName)
                    return 1

                else:
                    logger_smt.info('Fail! ADASL3 function is not OK!!!---%s' %ECUName)
                    return 0
            else:
                logger_smt.info('Fail! ADASL3 - wrong ECU Partnum!---%s' %ECUName)
                return 0

def SleepCurrent():
    '''计算睡眠模式下的电流值
        返回：1——正常；0——异常'''
    pc.power_on()
    rc.ign_on()
    time.sleep(1)
    pc.voltage_set_12()
    rc.ign_off()
    thr_2dc.stop()
    thr_35a.stop()
    thr_375.stop()
    time.sleep(10)
    statime = time.time()
    while True:
        sleepcurrent = pc.current_meas()
        if sleepcurrent <= 0.002:
            break
        if time.time() - statime > 10:
            break
    if sleepcurrent > 0.002:
        logger_smt.info('Fail! current>0.001 in sleep mode. current=%.3f' % sleepcurrent)
        thr_2dc.restart()
        thr_35a.restart()
        thr_375.ignon_run()
        # rc.ign_on()
        return 0
    else:
        logger_smt.info('Pass! current<0.001 in sleep mode')
        thr_2dc.restart()
        thr_35a.restart()
        thr_375.ignon_run()
        # rc.ign_on()
        return 1


def time_sh_del():
    '''关闭进程并删除time.sh
        '''
    if Config_list["connection"] == "Serial":
        j2_ser = serial.Serial(Config_list["com_port_j2"], 115200)
        j2_ser.timeout = 0.5
        j2_ser.writeTimeout = 0.5
        j2_ser.write(b'root\n')
        j2_ser.write(b'\n')
        time.sleep(1)
        j2_ser.write(b'root\n')
        time.sleep(1)
        # j2_ser.write(b'ps\n')
        # flag_spi, flag_watchdog, flag_opt = 1, 1, 1
        # while flag_spi | flag_watchdog | flag_opt:
        #     j2log = j2_ser.readline().decode("utf8", "ignore").strip()
        #     if ('spi_service' in j2log):
        #         pid_spi = j2log.split()[0]
        #         flag_spi = 0
        #     elif ('{watchdog.sh} /bin/sh ./watchdog.sh' in j2log):
        #         pid_watchdog = j2log.split()[0]
        #         flag_watchdog = 0
        #     elif ('/operation-app'in j2log):
        #         pid_opt = j2log.split()[0]
        #         flag_opt = 0
        # j2_ser.write(b'\n')
        # j2_ser.write(b'kill -9 %s\n' % pid_spi.encode())
        # j2_ser.write(b'kill -9 %s\n' % pid_watchdog.encode())
        # j2_ser.write(b'kill -9 %s\n' % pid_opt.encode())
        j2_ser.write(b'rm -rf /userdata/ota/time.sh\n')
        j2_ser.write(b'cat /userdata/ota/time.sh\n')
        time_start = time.time()
        flag = 1
        while flag:
            j2log = j2_ser.readline().decode("utf8", "ignore").strip()
            if ('No such file or directory' in j2log):
                logger_smt.info('time.sh is deleted(Serial)')
                break
            if time.time()-time_start > 3:
                flag = 0
                logger_smt.info('Warning! time.sh is not deleted')
    elif (Config_list["connection"] == "SSH"):
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        with suppress(paramiko.ssh_exception.AuthenticationException):
            ssh_client.connect(hostname="10.0.0.34",
                               username='root', password='')
        ssh_client.get_transport().auth_none(username='root')
        stdin, stdout, stderr = ssh_client.exec_command('ps')
        ssh_content = ssh_content = stdout.readlines()
        flag_spi, flag_watchdog, flag_opt = 1, 1, 1
        for i in ssh_content:
            if ('spi_service' in i):
                pid_spi = i.split()[0]
            elif ('{watchdog.sh} /bin/sh ./watchdog.sh' in i):
                pid_watchdog = i.split()[0]
            elif ('/operation-app'in i):
                pid_opt = i.split()[0]
        ssh_client.exec_command('kill -9 %s\n' % pid_spi)
        ssh_client.exec_command('kill -9 %s\n' % pid_watchdog)
        ssh_client.exec_command('kill -9 %s\n' % pid_opt)
        ssh_client.exec_command('rm -rf /userdata/ota/time.sh\n')
        ssh_client.exec_command('cat /userdata/ota/time.sh\n')
        stdin, stdout, stderr = ssh_client.exec_command(
            'cat /userdata/ota/time.sh')
        ssh_content = stdout.readlines()
        for i in ssh_content:
            if 'date -s' in i:
                logger_smt.info('Warning! time.sh ist not deleted')
        if ssh_content == []:
            logger_smt.info("time.sh is deleted(SSH)")
        ssh_client.close()


def GERJ2time():
    # 自动化测试_发送时间报文后，读取j2 time.sh内容
    # 计算当前日期，用于和time.sh中存储的日期进行比较
    '''返回：1——正常；0——异常'''
    pc.power_on()
    pc.voltage_set_12()
    time.sleep(0.1)
    CANClear()
    rc.ign_on()
    
    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    if month[0] == '0':
        month = month[1]
    day = datetime.datetime.now().strftime('%d')
    if day[0] == '0':
        day = day[1]
    date = year + '-' + month + '-' + day

    # 关闭进程，删除time.sh并重新上电
    time.sleep(15)
    time_sh_del()
    rc.kl30_off()
    time.sleep(1)
    rc.kl30_on()
    time.sleep(10)

    can_id = 0x35a
    can_data = datetime_hex()
    can_data.extend([0x00, 0x00, 0x00])
    Rx_start = time.time()
    while True:
        send_one(can_id, can_data)
        time.sleep(1)
        if time.time() - Rx_start > 3:
            break
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
        j2_ser.write(b'cat /userdata/ota/time.sh\n')
        while True:
            j2log = j2_ser.readline().decode("utf8", "ignore").strip()
            if ('date -s' in j2log):
                date_time = j2log.split('"')[1]
                if date in date_time:
                    logger_smt.info('Pass! time.sh is automatically generated %s' % date_time)
                    j2_ser.close()
                    return 1
                else:
                    logger_smt.info('Fail! date is wrong')
                    j2_ser.close()
                    return 0
            elif ('No such file or directory' in j2log):
                logger_smt.info("Fail! No such file: time.sh")
                j2_ser.close()
                return 0
                
    else:
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        with suppress(paramiko.ssh_exception.AuthenticationException):
            ssh_client.connect(hostname="10.0.0.34",
                               username='root', password='')
        ssh_client.get_transport().auth_none(username='root')
        stdin, stdout, stderr = ssh_client.exec_command(
            'cat /userdata/ota/time.sh')
        ssh_content = stdout.readlines()
        for i in ssh_content:
            if 'date -s' in i:
                date_time = i.split('"')[1]
                if date in date_time:
                    logger_smt.info('Pass! time.sh is automatically generated %s' % date_time)
                    ssh_client.close()
                    return 1
                else:
                    logger_smt.info('Fail! date is wrong')
                    ssh_client.close()
                    return 0

        if ssh_content == []:
            logger_smt.info("Fail! No such file: time.sh")
            ssh_client.close()
            return 0

        ssh_client.close()

def datetime_hex():
    '''获取系统时间并按照com报文要求的格式转换成十六进制
    参考layout
    '''
    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')
    hour = datetime.datetime.now().strftime('%H')
    minute = datetime.datetime.now().strftime('%M')
    second = datetime.datetime.now().strftime('%S')
    # 第一行
    year = (int(year))
    year = year % 100
    num1_hex = hex(year)
    # print(num1_hex)
    # 第二行
    month = int(month)
    month4 = month >> 3 & 1
    month3 = month >> 2 & 1
    month2 = month >> 1 & 1
    month1 = month >> 0 & 1
    day = int(day)
    day5 = day >> 4 & 1
    day4 = day >> 3 & 1
    day3 = day >> 2 & 1
    day2 = day >> 1 & 1
    num2 = day2*1+day3*2+day4*4+day5*8+month1*16+month2*32+month3*64+month4*128
    num2_hex = hex(num2)
    # print(num2_hex)
    # 第三行
    day1 = day >> 0 & 1
    hour = int(hour)
    hour5 = hour >> 4 & 1
    hour4 = hour >> 3 & 1
    hour3 = hour >> 2 & 1
    hour2 = hour >> 1 & 1
    hour1 = hour >> 0 & 1
    minute = int(minute)
    minute6 = minute >> 5 & 1
    minute5 = minute >> 4 & 1
    num3 = minute5*1+minute6*2+hour1*4+hour2*8+hour3*16+hour4*32+hour5*64+day1*128
    num3_hex = hex(num3)
    # print(num3_hex)
    # 第四行
    minute4 = minute >> 3 & 1
    minute3 = minute >> 2 & 1
    minute2 = minute >> 1 & 1
    minute1 = minute >> 0 & 1
    second = int(second)
    second6 = second >> 5 & 1
    second5 = second >> 4 & 1
    second4 = second >> 3 & 1
    second3 = second >> 2 & 1
    num4 = second3+second4*2+second5*4+second6*8 + \
        minute1*16+minute2*32+minute3*64+minute4*128
    num4_hex = hex(num4)
    # print(num4_hex)
    # 第五行
    second2 = second >> 1 & 1
    second1 = second >> 0 & 1
    num5 = second1*64+second2*128
    num5_hex = hex(num5)
    # print(num5_hex)
    return [int(num1_hex, 16), int(num2_hex, 16), int(num3_hex, 16), int(num4_hex, 16), int(num5_hex, 16)]

