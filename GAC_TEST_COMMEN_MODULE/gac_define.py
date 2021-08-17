# Description : 测试软件架构-通用宏定义及全局变量
# Author : Yida.Wang
# Editor :
# Revision History
# Version       Data         Initials          Description
#  V1.0       20210726      Yida.Wang           Original
import os
# 宏定义
TIME_DTC_RECORD = 1   # 默认故障设置时间为100ms，按照1s，保证故障设置完成
TIME_DTC_CLEAR = 1    # 软件未设置故障恢复时间，按照1s，保证故障恢复完成
TIME_DTC_RECORD_LC_35A = 4  # 节点丢失故障设置时间为6*报文周期+100ms，ICM节点报文周期500ms，故障设置时间为3.1s
TIME_DTC_RECORD_LC_2DC = 1  # 同上，ADAS节点报文周期100ms，故障设置时间为700ms
TIME_DTC_CLEAR_LC_35A = 5   # 节点丢失故障恢复时间为5s
TIME_DTC_CLEAR_WAIT = 0.5   # DTC清除后的等待时间
TEST_FAILED = 1
CONFIRMED_DTC = 8
ALL_DTC = 9
# dtc_str
DTC_HIGH_VOL = 'af0817'
DTC_LOW_VOL = 'af0816'
DTC_LOST_COM_ICM = 'c18487'
DTC_LOST_COM_ADAS = 'd24087'
DTC_BUS_OFF = 'c07388'
DTC_OMS_Powerfailure = 'af0f77'
DTC_DMS_Powerfailure = 'af0f76'
DTC_Ethernet_Timeout = 'af0f87'
DTC_Loss_DMS_LVDS = 'af0a87'
DTC_Loss_OMS_LVDS = 'af0b87'
# dtc
DTC_HIGH_VOL_HEX = 0xaf0817
DTC_LOW_VOL_HEX = 0xaf0816
DTC_LOST_COM_ICM_HEX = 0xc18487
DTC_LOST_COM_ADAS_HEX = 0xd24087
DTC_BUS_OFF_HEX = 0xc07388
DTC_OMS_Powerfailure_HEX = 0xaf0f77
DTC_DMS_Powerfailure_HEX = 0xaf0f76
DTC_Ethernet_Timeout_HEX = 0xaf0f87
DTC_Loss_DMS_LVDS_HEX = 0xaf0a87
DTC_Loss_OMS_LVDS_HEX = 0xaf0b87
# global var
IGN_I = 1
dtc = 0
path = os.path.dirname(os.path.abspath(__file__))
PATH_FLS = path + '\\DMS_FlashDrv.bin'
PATH_APP_T = path + '\\DMS_TEST_APP.bin'
PATH_APP_C = path + '\\DMS_B00_APP.bin'
# 初始化表示can总线的全局变量, bus1是专门用于记录log的通道
from can.interfaces.zlgcan import zlgcanBus
bus0 = zlgcanBus(channel=0, device=0, bitrate=500000)
bus1 = zlgcanBus(channel=1, device=0, bitrate=500000)
# 用test_logger记录全部can报文信息及故障记录及解除时间，作为给测试部的log信息
toppath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import logging
# 记录测试中全部报文
log_format = logging.Formatter('%(asctime)s - %(message)s')
level = 9
handler_test = logging.FileHandler(filename = toppath + '\\TESTLOG\\GAC_TEST.log', mode = 'w')
handler_test.setFormatter(log_format)
test_logger = logging.getLogger('GAC_TEST_Log')
test_logger.setLevel(level)
test_logger.addHandler(hdlr = handler_test)
# 记录冒烟测试log
log_format_smt = logging.Formatter('%(message)s')
level = 9
handler_smt = logging.FileHandler(filename = toppath + '\\TESTLOG\\SMT_RESULT.log', mode = 'w')
handler_smt.setFormatter(log_format_smt)
logger_smt = logging.getLogger('GAC_SMT_Log')
logger_smt.setLevel(level)
logger_smt.addHandler(hdlr = handler_smt)

