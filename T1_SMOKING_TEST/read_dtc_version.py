# Description : dtc测试，读版本
# Author : Zengzeng.Duan
# Editor : Yida.Wang
# Revision History
# Version       Data         Initials          Description
#  V1.0       20210810      Zengzeng.Duan        Original
#  V1.1       20210812       Yida.Wang         1. 增加错误11次程序自动退出 
#                                              2. 增加svnversion及supplier swversion缺失的错误处理
#                                              3. 使用logger_smt记录log
from canrxtx import CANRead1000, recv
from GAC_TEST_COMMEN_MODULE.external_device import *
from GAC_TEST_COMMEN_MODULE.gac_test_uds import *
from GAC_TEST_COMMEN_MODULE.gac_define import *
from GAC_TEST_COMMEN_MODULE.fault_maker import *

def ReadDTC():
    '''测DTC'''
    pc.power_off()
    time.sleep(1)
    pc.power_on()
    pc.voltage_set_12()
    CANRead1000()
    rc.ign_on()
    while True:
        msg = recv()
        if msg != None:
            break
        else:
            time.sleep(1)
            rc.ign_on()
    # thr_375 = Thread_send_375()
    # thr_35a = Thread_send_35a()
    # thr_2dc = Thread_send_2dc()
    # thr_375.start()
    # time.sleep(10)
    # thr_35a.start()
    # thr_2dc.start()
    # time.sleep(5)
    uc = uds_client().client_connect()
    with uc as client:
        while True:
            try:           
                client.clear_dtc()
                break
            except:
                pass
        time.sleep(15)
        while True:
            try:           
                dtc_num = client.get_number_of_dtc_by_status_mask(0xff)
                break
            except:
                pass      
        dtc_num = int((dtc_num.data.hex()[8:]), 16)
        # print(dtc_num)
        if dtc_num == 0:
            logger_smt.info('Pass! No DTC')
            thr_35a.stop()
            thr_2dc.stop()
            thr_375.stop()
            # pc.power_off()
            return 1
        else:
            logger_smt.info('Fail! number of DTC is: %d' % dtc_num)

            while True:
                try:           
                    dtc_status = client.get_dtc_by_status_mask(0xff)
                    break
                except:
                    pass
            dtc_status = dtc_status.data.hex()[4:]
            logger_smt.info(dtc_status)  # c184872aaf1f202b
            for i in range(dtc_num):
                if dtc_status[i*8:i*8+6] == "c07388":
                    logger_smt.info('CAN BUS OFF. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                elif dtc_status[i*8:i*8+6] == "af0f76":
                    logger_smt.info('DMS Camera failure. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                elif dtc_status[i*8:i*8+6] == "af1f09":
                    logger_smt.info('DMS software version mismatch. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                elif dtc_status[i*8:i*8+6] == "af1f20":
                    logger_smt.info('ECU Internal electronic failure. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                elif dtc_status[i*8:i*8+6] == "af0f87":
                    logger_smt.info('Ethernet Timeout Global Timeout. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                elif dtc_status[i*8:i*8+6] == "af0a87":
                    logger_smt.info('Loss of DMS Camera LVDS Communication. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                elif dtc_status[i*8:i*8+6] == "af0b87":
                    logger_smt.info('Loss of OMS Camera LVDS Communication. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                elif dtc_status[i*8:i*8+6] == "af0f77":
                    logger_smt.info('OMS Camera failure. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                elif dtc_status[i*8:i*8+6] == "c18487":
                    logger_smt.info('lost communication with ICM. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                elif dtc_status[i*8:i*8+6] == "af0817":
                    logger_smt.info('system voltage abnormal high. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                elif dtc_status[i*8:i*8+6] == "af0816":
                    logger_smt.info('system voltage abnormal low. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                elif dtc_status[i*8:i*8+6] == "d24087":
                    logger_smt.info('lost communication with ADAS_FRR_1. status bit: %s' %
                          dtc_status[i*8+6:i*8+8])
                else:
                    logger_smt.info('DTC definition is not enough.')
            # thr_35a.stop()
            # thr_2dc.stop()
            # thr_375.stop()
            # pc.power_off()
            return 0

def ReadVersion():
    '''读取版本号'''
    pc.power_on()
    rc.ign_on()
    pc.voltage_set_12()
    time.sleep(0.1)
    flag_exit = 0
    while True:
        try:
            uc = uds_client().client_connect()
            with uc as client:
                SwVerison = client.read_data_by_identifier(0xf189).service_data.values[0xf189]
                HWVerison = client.read_data_by_identifier(0xf17f).service_data.values[0xf17f]
                AppVerison = client.read_data_by_identifier(0xf181).service_data.values[0xf181]
                BTVerison = client.read_data_by_identifier(0xf180).service_data.values[0xf180]
                Partnum = client.read_data_by_identifier(0xf187).service_data.values[0xf187]
                try:
                    SVNVersion = client.read_data_by_identifier(0x0E30).service_data.values[0x0E30]
                except:
                    SVNVersion = '----'
                    logger_smt.info('No SVNVersion')
                GACSumVersion = client.read_data_by_identifier(0xf18E).service_data.values[0xf18E]
                ECUVersion = client.read_data_by_identifier(0xf197).service_data.values[0xf197]
                try:
                    Sup_SwVersion = client.read_data_by_identifier(0xF195).data.hex()[4:]
                except:
                    Sup_SwVersion = '----'
                    logger_smt.info('No Supplier SwVersion')
            break
        except:
            flag_exit += 1
            if flag_exit > 10:
                rc.ign_off()
                pc.power_off()
                exit(0)
    
    desc = u'零件号：(%s)\n软件版本号: (%s)\n硬件版本号: (%s)\nAPP版本号:(%s)\nBT版本号：(%s)\n内部版本号：(%s)\nSVN版本号：(%s)\n广汽总成零件号：(%s)\nECU零件号：(%s)\n' % (
        Partnum, SwVerison, HWVerison, AppVerison, BTVerison, Sup_SwVersion, SVNVersion, GACSumVersion, ECUVersion)
    print(desc)
    logger_smt.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logger_smt.info(desc)
    version = [Partnum, SwVerison, HWVerison, AppVerison, BTVerison, Sup_SwVersion, SVNVersion, GACSumVersion, ECUVersion]
    return [version, desc]


