# Description : 测试软件架构-功能抽象层-外部设备模块
# 电源配置、控制及继电器控制，导入配置文件，并生成电源及继电器的全局变量
# Author : Yida.Wang
# Editor :
# Revision History
# Version       Data             Initials                                    Description
#  V1.0       20210726          Yida.Wang                                      Original
#  V1.1       20210812      Yida.Wang, Zengzeng.Duan     1.增加电源类中功率及电流测量方法，增加常用电压设置;
#                                                        2.删除korad电源设置电流的部分及延时;
import serial
import time
import ctypes
import json
import os

class JsonConf:
    '''json配置文件类'''
    @staticmethod
    def load(config_name):
        if not os.path.exists(config_name):
            with open(config_name, 'w') as json_file:
                pass
        with open(config_name) as json_file:
            try:
                dic_config = json.load(json_file)
            except:
                dic_config = {}
            return dic_config

class Power_control:
    def __init__(self, Config_list):
        '''电源串口通信初始化
        '''
        self.power_source_name = Config_list["power_source_name"]
        self.ser = serial.Serial(Config_list["com_port"])
        self.ser.timeout=0.5
        self.ser.writeTimeout=0.5
    def voltage_set_12(self):
        '''设置电源电压12V
        '''
        if self.power_source_name == "RIGOL":
            self.ser.write(b':APPLy CH1,12,2\n')
        else:
            self.ser.write(b'VSET1:12')
    def voltage_set_18_5(self):
        '''设置电源电压18.5V
        '''
        if self.power_source_name == "RIGOL":
            self.ser.write(b':APPLy CH1,18.5,2\n')
        else:
            self.ser.write(b'VSET1:18.5')
    def voltage_set_17(self):
        '''设置电源电压17V
        '''
        if self.power_source_name == "RIGOL":
            self.ser.write(b':APPLy CH1,17,2\n')
        else:
            self.ser.write(b'VSET1:17')
    def voltage_set_8(self):
        '''设置电源电压8V
        '''
        if self.power_source_name == "RIGOL":
            self.ser.write(b':APPLy CH1,8,2\n')
        else:
            self.ser.write(b'VSET1:8')
    def voltage_set_6_5(self):
        '''设置电源电压6.5V
        '''
        if self.power_source_name == "RIGOL":
            self.ser.write(b':APPLy CH1,6.5,2\n')
        else:
            self.ser.write(b'VSET1:6.5')
    def voltage_set_6(self):
        '''设置电源电压6V
        '''
        if self.power_source_name == "RIGOL":
            self.ser.write(b':APPLy CH1,6,2\n')
        else:
            self.ser.write(b'VSET1:6')
    def power_on(self):
        '''开启电源
        '''
        if self.power_source_name == "RIGOL":
            self.ser.write(b':OUTPut:STATe CH1,ON\n')
        else:
            self.ser.write(b'OUT1')
    def power_off(self):
        '''关闭电源
        '''
        if self.power_source_name == "RIGOL":             # 关闭继电器
            self.ser.write(b':OUTPut:STATe CH1,OFF\n')  # 关闭电源
        else:
            self.ser.write(b'OUT0')
    def voltage_set(self, voltage, current = b'2'):
        '''使用举例:Power_control().voltage_set(b'12',b'2')
        注意: 对于Korad电源，首先设置电流，后设置电压，有0.1s延迟
        '''
        if self.power_source_name == "RIGOL":
            self.ser.write(b':APPLy CH1,%s,%s\n' %(voltage, current))
        else:
            self.ser.write(b'ISET1:%s' %current)
            time.sleep(0.1)
            self.ser.write(b'VSET1:%s' %voltage)
    def power_meas(self):
        '''检查ECU功率;返回功率值
        '''
        # 测量功率
        if self.power_source_name == "RIGOL":
            self.ser.write(b':MEASure:POWEr? CH1\n')
            power_ecu = self.ser.readline().decode().strip()
        else:
            self.ser.write(b'IOUT1?')
            current = self.ser.readline().decode().strip()
            self.ser.write(b'VOUT1?')
            voltage = self.ser.readline().decode().strip()
            power_ecu = float(current)*float(voltage)
        return float(power_ecu)
    def current_meas(self):
        '''检查ECU电流;返回电流值
        '''
        # 测量功率
        if self.power_source_name == "RIGOL":
            self.ser.write(b':MEASure:CURRent?\n')
            current_ecu = self.ser.readline().decode().strip()
        else:
            self.ser.write(b'IOUT1?')
            current_ecu = self.ser.readline().decode().strip()
        return float(current_ecu)

class Relay_control:
    '''用于usb继电器控制：注意由于继电器外接连线原因导致：
       继电器1闭合，KL30断开；
       继电器2闭合，IGN连接；
    '''
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.objdll = ctypes.windll.LoadLibrary('%s/usbrelay.dll' %path)    # 使用usb继电器需要的动态链接库
        self.hdl = self.objdll.USBRELAY_Open(1)
    def kl30_off(self):
        self.objdll.USBRELAY_SetRelay(self.hdl, 1, 1)                # 闭合继电器端口1开关，断开KL30
    def kl30_on(self):
        self.objdll.USBRELAY_SetRelay(self.hdl, 1, 0)                # 断开继电器端口1开关，闭合KL30
    def ign_on(self):
        self.objdll.USBRELAY_SetRelay(self.hdl, 2, 1)                # 闭合继电器端口2开关，连接IGN
    def ign_off(self):
        self.objdll.USBRELAY_SetRelay(self.hdl, 2, 0)                # 断开继电器端口2开关，断开IGN

Config_list = JsonConf.load("config.json")
pc = Power_control(Config_list)
rc = Relay_control()
