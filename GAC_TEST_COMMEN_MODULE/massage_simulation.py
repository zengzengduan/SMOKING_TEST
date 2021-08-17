# Description : 测试软件架构-功能抽象层-报文模拟模块
# 模拟报文发送
# Author : Yida.Wang
# Editor :
# Revision History
# Version       Data         Initials          Description
#  V1.0       20210726      Yida.Wang           Original
import threading
import can
import time
from .gac_define import bus0
from .gac_define import bus1
from .gac_define import test_logger
# 全局变量
_FINISH_375 = False
_FINISH_35a = False
_FINISH_2dc = False
_FINISH_3e00 = False
_FINISH_3e80 = False
_FINISH_510 = False
_FINISH_rcv = False
# 模块内部变量

class Thread_send_375(threading.Thread):
    def __init__(self, timeout=1.0):
        super(Thread_send_375, self).__init__()
        self.timeout = timeout
        self.data = [0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    def run(self):
        def send_mes_375():
            global _FINISH_375
            global bus0
            msg = can.Message(arbitration_id=0x375, is_extended_id=0, data=self.data)
            while True:
                bus0.send(msg)
                time.sleep(0.02)
                if _FINISH_375 == True:
                    break
        subthread = threading.Thread(target=send_mes_375, args=())
        subthread.setDaemon(True)
        subthread.start()
    def setvalue(self, data):
        self.data = data
    def stop(self):
        global _FINISH_375
        _FINISH_375 = True
        self.join()
    def crank_run(self):
        global _FINISH_375
        _FINISH_375 = False
        self.setvalue(data=[0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.run()
    def ignon_run(self):
        global _FINISH_375
        _FINISH_375 = False
        self.setvalue(data=[0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.run()
    def ignoff_run(self):
        global _FINISH_375
        _FINISH_375 = False
        self.setvalue(data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.run()
    def acc_run(self):
        global _FINISH_375
        _FINISH_375 = False
        self.setvalue(data=[0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.run()
    
class Thread_send_35a(threading.Thread):
    def __init__(self, timeout=1.0):
        super(Thread_send_35a, self).__init__()
        self.timeout = timeout
    def run(self):
        def send_mes_35a():
            global _FINISH_35a
            global bus0
            msg = can.Message(arbitration_id=0x35a, is_extended_id=0, data=[0x15, 0x34, 0xce, 0x00, 0x00, 0x00, 0x00, 0x00])
            while True:
                bus0.send(msg)
                time.sleep(0.2)
                if _FINISH_35a == True:
                    break
        subthread = threading.Thread(target=send_mes_35a, args=())
        subthread.setDaemon(True)
        subthread.start()
    def stop(self):
        global _FINISH_35a
        _FINISH_35a = True
        self.join()
    def restart(self):
        global _FINISH_35a
        _FINISH_35a = False
        self.run()

class Thread_send_2dc(threading.Thread):
    def __init__(self, timeout=1.0):
        super(Thread_send_2dc, self).__init__()
        self.timeout = timeout
    def run(self):
        def send_mes_2dc():
            global _FINISH_2dc
            global bus0
            msg = can.Message(arbitration_id=0x2dc, is_extended_id=0, data=[0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            while True:
                bus0.send(msg)
                time.sleep(0.1)
                if _FINISH_2dc == True:
                    break
        subthread = threading.Thread(target=send_mes_2dc, args=())
        subthread.setDaemon(True)
        subthread.start()
    def stop(self):
        global _FINISH_2dc
        _FINISH_2dc = True
        self.join()
    def restart(self):
        global _FINISH_2dc
        _FINISH_2dc = False
        self.run()

class Thread_send_3e00(threading.Thread):
    def __init__(self, timeout=1.0):
        super(Thread_send_3e00, self).__init__()
        self.timeout = timeout
    def run(self):
        def send_mes_3e00():
            global bus0
            global _FINISH_3e00
            msg = can.Message(arbitration_id=0x722, is_extended_id=0, data=[0x02, 0x3e, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00])
            while True:
                bus0.send(msg)
                time.sleep(4)
                if _FINISH_3e00 == True:
                    break
        subthread = threading.Thread(target=send_mes_3e00, args=())
        subthread.setDaemon(True)
        subthread.start()
    def stop(self):
        global _FINISH_3e00
        _FINISH_3e00 = True
        self.join()
    def restart(self):
        global _FINISH_3e00
        _FINISH_3e00 = False
        self.run()

class Thread_send_3e80(threading.Thread):
    def __init__(self, timeout=1.0):
        super(Thread_send_3e80, self).__init__()
        self.timeout = timeout
    def run(self):
        def send_mes_3e80():
            global bus0
            global _FINISH_3e80
            msg = can.Message(arbitration_id=0x722, is_extended_id=0, data=[0x02, 0x3e, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00])
            while True:
                bus0.send(msg)
                time.sleep(2)
                if _FINISH_3e80 == True:
                    break
        subthread = threading.Thread(target=send_mes_3e80, args=())
        subthread.setDaemon(True)
        subthread.start()
    def stop(self):
        global _FINISH_3e80
        _FINISH_3e80 = True
        self.join()
    def restart(self):
        global _FINISH_3e80
        _FINISH_3e80 = False
        self.run()

class Thread_send_510(threading.Thread):
    def __init__(self, timeout=1.0):
        super(Thread_send_510, self).__init__()
        self.timeout = timeout
    def run(self):
        def send_mes_510():
            global _FINISH_510
            global bus0
            msg = can.Message(arbitration_id=0x510, is_extended_id=0, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            while True:
                bus0.send(msg)
                time.sleep(0.2)
                if _FINISH_510 == True:
                    break
        subthread = threading.Thread(target=send_mes_510, args=())
        subthread.setDaemon(True)
        subthread.start()
    def stop(self):
        global _FINISH_510
        _FINISH_510 = True
        self.join()
    def restart(self):
        global _FINISH_510
        _FINISH_510 = False
        self.run()

class Thread_rcv(threading.Thread):
    def __init__(self, test_logger):
        super(Thread_rcv, self).__init__()
        self.cm_logger = test_logger
    def run(self):
        def rcv():
            global bus1
            global _FINISH_rcv
            while True:
                recv = bus1.recv()
                self.cm_logger.info(recv)
                # logger.info(recv)
                if _FINISH_rcv == True:
                    break
        subthread = threading.Thread(target=rcv, args=())
        subthread.setDaemon(True)
        subthread.start()
    def stop(self):
        global _FINISH_rcv
        _FINISH_rcv = True
        self.join()
    def restart(self):
        global _FINISH_rcv
        _FINISH_rcv = False
        self.run()

thr_375 = Thread_send_375()
thr_35a = Thread_send_35a()
thr_2dc = Thread_send_2dc()
thr_3e00 = Thread_send_3e00()
thr_3e80 = Thread_send_3e80()
thr_510 = Thread_send_510()
thr_cm = Thread_rcv(test_logger)