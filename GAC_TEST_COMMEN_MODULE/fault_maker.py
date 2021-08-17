# Description : 测试软件架构-功能抽象层-故障模拟模块
# 制造和清除故障，使用类makefault和clearfault
# Author : Yida.Wang
# Editor :
# Revision History
# Version       Data         Initials          Description
#  V1.0       20210726      Yida.Wang           Original
import win32api
import win32con
from .massage_simulation import *
from .external_device import *
from .gac_define import test_logger

class makefault:
    @staticmethod
    def high_voltage(pc):
        pc.voltage_set_17()
        test_logger.info('High voltage')
    @staticmethod
    def low_voltage(pc):
        pc.voltage_set_8()
        test_logger.info('Low voltage')
    @staticmethod   
    def loss_com_icm(thr):
        thr.stop()
        test_logger.info('lost communication with ICM')
    @staticmethod
    def loss_com_adas(thr):
        thr.stop()
        test_logger.info('lost communication with ADAS')
    @staticmethod
    def loss_lvds_oms():
        win32api.MessageBox(0, "请拔掉OMS视频输入线", "提醒",win32con.MB_OK)
        # input('请拔掉OMS视频输入线, 完成后按回车')
        test_logger.info('Loss of OMS Camera LVDS Communication')
    @staticmethod
    def loss_lvds_dms():
        win32api.MessageBox(0, "请拔掉DMS视频输入线", "提醒",win32con.MB_OK)
        # input('请拔掉DMS视频输入线, 完成后按回车')
        test_logger.info('Loss of DMS Camera LVDS Communication')
    @staticmethod
    def power_failure_oms():
        win32api.MessageBox(0, "请拔掉OMS电源线", "提醒",win32con.MB_OK)
        # input('请拔掉OMS电源线, 完成后按回车')
        test_logger.info('OMS Camera Power Supplyfailure')
    @staticmethod
    def power_failure_dms():
        win32api.MessageBox(0, "请拔掉DMS电源线", "提醒",win32con.MB_OK)
        # input('请拔掉DMS电源线, 完成后按回车')
        test_logger.info('DMS Camera Power Supplyfailure')
    @staticmethod
    def ethernet_timeout():
        win32api.MessageBox(0, "请拔掉以太网线", "提醒",win32con.MB_OK)
        # input('请拔掉以太网线, 完成后按回车')
        test_logger.info('Ethernet Timeout')
    
class clearfault:
    @staticmethod
    def high_voltage(pc):
        pc.voltage_set_12()
        test_logger.info('Fault ''Abnormal voltage'' is cleared')
    @staticmethod
    def low_voltage(pc):
        pc.voltage_set_12()
        test_logger.info('Fault ''Abnormal voltage'' is cleared')
    @staticmethod
    def loss_com_icm(thr):
        thr.restart()
        test_logger.info('Fault ''lost communication with ICM'' is cleared')
    @staticmethod
    def loss_com_adas(thr):
        thr.restart()
        test_logger.info('Fault ''lost communication with ADAS'' is cleared')
    @staticmethod
    def loss_lvds_oms():
        win32api.MessageBox(0, "请插上OMS视频输入线", "提醒",win32con.MB_OK)
        # input('请插上OMS视频输入线, 完成后按回车')
        test_logger.info('Fault ''Loss of OMS Camera LVDS Communication'' is cleared')
    @staticmethod
    def loss_lvds_dms():
        win32api.MessageBox(0, "请插上DMS视频输入线", "提醒",win32con.MB_OK)
        # input('请插上DMS视频输入线, 完成后按回车')
        test_logger.info('Fault ''Loss of DMS Camera LVDS Communication'' is cleared')
    @staticmethod
    def power_failure_oms():
        win32api.MessageBox(0, "请插上OMS电源线", "提醒",win32con.MB_OK)
        # input('请插上OMS电源线, 完成后按回车')
        test_logger.info('Fault ''OMS Camera Power Supplyfailure'' is cleared')
    @staticmethod
    def power_failure_dms():
        win32api.MessageBox(0, "请插上DMS电源线", "提醒",win32con.MB_OK)
        # input('请插上DMS电源线, 完成后按回车')
        test_logger.info('Fault ''DMS Camera Power Supplyfailure'' is cleared')
    @staticmethod
    def ethernet_timeout():
        win32api.MessageBox(0, "请插上以太网线", "提醒",win32con.MB_OK)
        # input('请插上以太网线, 完成后按回车')
        test_logger.info('Fault ''Ethernet Timeout'' is cleared')

        

