# Function : the smoke test of GAC Aeon Smart Cockpit Controller
# Notice :
# Author : zengzeng.duan
# Editor : Yida.Wang
# Revision History
# Version       Data         Initials             Description
#  V0.9       20210801      zengzeng.duan          Original
#  V1.0       20210812       Yida.Wang           修改头部import，审查代码，修改程序小问题
'''
Test module           |                  Function                |           From
——————————————————————————————————————————————————————————————————————————————————————————
ReadDTC               |                  测DTC                   |    read_dtc_version.py
ReadVersion           |                读取版本号                 |    read_dtc_version.py
CANPeriod             |           计算工作模式下报文周期           |       CANRxTx.py
PeriodIGNOff          |     IGN_Off情况下发送0x510,计算报文周期    |       CANRxTx.py
CANFlash              |                 CAN刷写                  |        flash.py
SPIFlash              |                 SPI刷写                  |        flash.py
WorkMode              |           测试工作模式是否正常             |      modeconvert.py
ComMode               |           测试通信模式是否正常             |      modeconvert.py
LowMode               |           测试低功耗模式是否正常           |      modeconvert.py
WorkMode              |        测试工作模式到通信模式的转换         |      modeconvert.py
ComToWork             |        测试通信模式到工作模式的转换         |      modeconvert.py
WorkToLow             |        测试工作模式到低功耗模式的转换       |      modeconvert.py
LowToWork             |        测试低功耗模式到工作模式的转换       |      modeconvert.py
LowToCom              |        测试低功耗模式到通信模式的转换       |      modeconvert.py
ComToLow              |        测试通信模式到低功耗模式的转换       |      modeconvert.py
CanToNoneVoltage      |            CAN报文消失电压值               |      modeconvert.py
NoneToCanVoltage      |            CAN报文出现电压值               |      modeconvert.py
CameraToNoneVoltage   |            摄像头消失电压值                |      modeconvert.py
NoneToCameraVoltage   |            摄像头出像电压值                |      modeconvert.py
IGN                   |              判断IGN是否正常              |        others.py
ADASL3                |      判断不同车型的ADASL3功能是否正常      |        others.py
SleepCurrent          |           计算睡眠模式下的电流值           |        others.py
GERJ2time             |          time.sh中存储的日期更新          |        others.py
'''
import unittest
import os
import sys
out = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(out)
from GAC_TEST_COMMEN_MODULE.HTMLTestRunner import HTMLTestRunner
from read_dtc_version import *
from canrxtx import *
from modeconvert import *
from flash import *
from others import *

class TestDemo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''初始化测试环境'''
        pc.power_on()
        rc.ign_on()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        '''结束测试'''
        time.sleep(1)
        pc.power_off()
        rc.ign_off()

    def setUp(self):
        pass

    def tearDown(self):
        print("do something after test : clean up.\n")

    def ReadDTC(self):
        """测DTC
            返回：1——正常；0——异常"""
        self.assertEqual(1, ReadDTC())

    def CANPeriod(self):
        '''计算工作模式下报文周期
            返回：1——正常；0——异常'''
        self.assertEqual(1, CANPeriod())

    def PeriodIGNOff(self):
        '''IGN_Off情况下发送0x510,计算报文周期
            返回：1——正常；0——异常'''
        self.assertEqual(1, PeriodIGNOff())

    def IGN(self):
        """判断IGN是否正常
            返回：1——正常；0——异常"""
        self.assertEqual(1, IGN())

    def ADASL3(self):
        """判断不同车型的ADASL3功能是否正常
            返回：1——正常；0——异常"""
        self.assertEqual(1, ADASL3(ECUName))

    def SleepCurrent(self):
        """计算睡眠模式下的电流值
            返回：1——正常；0——异常"""
        self.assertEqual(1, SleepCurrent())

    def GERJ2time(self):
        """time.sh中存储的日期更新
            返回：1——正常；0——异常"""
        self.assertEqual(1, GERJ2time())

    def SPIFlash(self):
        """SPI刷写
            返回：1——正常；0——异常"""
        self.assertEqual(1, SPIFlash())

    def CANFlash(self):
        """CAN刷写
            返回：1——正常；0——异常"""
        self.assertEqual(1, CANFlash())
    
    def WorkMode(self):
        """测试工作模式是否正常
            返回：1——正常；0——异常"""
        self.assertEqual(1, WorkMode())

    def ComMode(self):
        """测试通信模式是否正常
            返回：1——正常；0——异常"""
        self.assertEqual(1, ComMode())

    def LowMode(self):
        """测试低功耗模式是否正常
            返回：1——正常；0——异常"""
        self.assertEqual(1, LowMode())

    def WorkToCom(self):
        """测试工作模式到通信模式的转换
            返回：1——正常；0——异常"""
        self.assertEqual(1, WorkToCom())

    def ComToWork(self):
        """测试通信模式到工作模式的转换
            返回：1——正常；0——异常"""
        self.assertEqual(1, ComToWork())

    def WorkToLow(self):
        """测试工作模式到低功耗模式的转换
            返回：1——正常；0——异常"""
        self.assertEqual(1, WorkToLow())
    
    def LowToWork(self):
        """测试低功耗模式到工作模式的转换
            返回：1——正常；0——异常"""
        self.assertEqual(1, LowToWork())

    def LowToCom(self):
        """测试低功耗模式到通信模式的转换
            返回：1——正常；0——异常"""
        self.assertEqual(1, LowToCom())

    def ComToLow(self):
        """测试通信模式到低功耗模式的转换
            返回：1——正常；0——异常"""
        self.assertEqual(1, ComToLow())

    def CanToNoneVoltage(self):
        """CAN报文消失电压值
            返回：1——正常；0——异常"""
        self.assertEqual(1, CanToNoneVoltage())

    def NoneToCanVoltage(self):
        """CAN报文出现电压值
            返回：1——正常；0——异常"""
        self.assertEqual(1, NoneToCanVoltage())

    def CameraToNoneVoltage(self):
        """摄像头消失电压值
            返回：1——正常；0——异常"""
        self.assertEqual(1, CameraToNoneVoltage())

    def NoneToCameraVoltage(self):
        """摄像头出像电压值
            返回：1——正常；0——异常"""
        self.assertEqual(1, NoneToCameraVoltage())

    @unittest.skip("do't run as not ready")
    def test_skip(self):
        """Test method"""
        print("do something before test : prepare environment.\n")

def getnowtime():  # 该方法获取当前最新时间
    return time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))

if __name__ == '__main__':
    thr_cm.start()
    verdesc = ReadVersion()
    ECUPartnum = verdesc[0][-1]
    ECUName = ECUPartnum[:7]
    report_title = verdesc[0][-1] + '---冒烟测试报告'
    filepath = os.path.join(os.getcwd(), 'Report', getnowtime() + ECUName+ '_SMKTReport.html')  # os.getcwd()获取当前的路径
    fp = open(filepath, 'wb')
    thr_375.start()
    thr_35a.start()
    thr_2dc.start()
    suite = unittest.TestSuite()
    tests = [
                TestDemo("setUpClass"),
                TestDemo("GERJ2time"),
                TestDemo("CANPeriod"),
                TestDemo("ADASL3"),
                TestDemo("PeriodIGNOff"),
                TestDemo("SleepCurrent"),
                TestDemo("ReadDTC"),
                TestDemo("WorkMode"),
                TestDemo("ComMode"),
                TestDemo("LowMode"),
                TestDemo("WorkToCom"),
                TestDemo("ComToWork"),
                TestDemo("WorkToLow"),
                TestDemo("LowToWork"),
                TestDemo("LowToCom"),
                TestDemo("ComToLow"),
                TestDemo("CanToNoneVoltage"),
                TestDemo("NoneToCanVoltage"),
                TestDemo("CameraToNoneVoltage"),
                TestDemo("NoneToCameraVoltage"),
                TestDemo("IGN"), 
                TestDemo("CANFlash"),        
                TestDemo("SPIFlash"),
                TestDemo("tearDownClass")
            ]
    suite.addTests(tests)
    runner = HTMLTestRunner(stream=fp, title=report_title, description=verdesc[1])
    runner.run(suite)
    thr_35a.stop()
    thr_2dc.stop()
    thr_375.stop()
    fp.close()
    thr_cm.stop()
