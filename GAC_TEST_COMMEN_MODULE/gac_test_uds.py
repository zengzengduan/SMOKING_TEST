# Description : 测试软件架构-功能抽象层-UDS调用模块
# Author : Yida.Wang
# Editor :
# Revision History
# Version       Data         Initials          Description
#  V1.0       20210726      Yida.Wang           Original
import udsoncan
import struct
import isotp
import datetime
import numpy as np
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import udsoncan.configs
from .gac_define import *

def SecureAlgo(seed, level):
   if level == 1: # App unlock level
      constant = np.uint32(0xE8D59AC7)
   elif level == 17:# BT unlock level
      constant = np.uint32(0x6EB5FCA0)
   else :
      print("Unkown unlock level")
   result = np.uint32(0)
   upack = struct.unpack('>L',seed)[0]
   u32seed = np.uint32(upack)
   rightshift  = np.uint32(u32seed  >> 9)
   leftshift = np.uint32(u32seed << 22)
   result =  rightshift | leftshift
   result = np.uint32(result)
   result *=6
   result = np.uint32(result)
   result ^=constant
   result = np.uint32(result)
   leftshift = np.uint32(result << 14)
   rightshift = np.uint32(result >> 17)
   result = leftshift | rightshift
   result = np.uint32(result)
   return struct.pack('>L',result)

class DID0x0E27J2JuncTemp(udsoncan.DidCodec):
    def encode(self, val):
        packed = struct.pack('<B', val)
        return packed
    def decode(self, payload):
        J2Temperature = struct.unpack('<B', payload)[0] - 40
    #   print("J2Temperature =%d"%J2Temperature)
        return
    def __len__(self):
        return 1

class DID0xF195SupplierECUSoftwareVer(udsoncan.DidCodec):
    def encode(self, val):
        pass
    def decode(self, payload):
        SupplierECUSoftwareVer = struct.unpack('<H', payload)[0] 
        return
    def __len__(self):
        return 2    

class DID0x0404ECUTemp(udsoncan.DidCodec):
    def encode(self, val):
      packed = struct.pack('>H', val)
      return packed
    def decode(self, payload):
        ECUTemp = struct.unpack('>H', payload)[0] - 40
        # print("ECUTemp =%f"%ECUTemp)
        return
    def __len__(self):
        return 2

class DID0x0E17SPIFaultCode(udsoncan.DidCodec):
    def encode(self, val):
        return
    def decode(self, payload):
        SPIFault  = struct.unpack('<B', payload)[0]
        # print(SPIFault)
        # if SPIFault & 0x01 != 0:
        #     print('Link Build Failure')
        # if SPIFault & 0x02 != 0:
        #     print('Handshake Build failure')
        # if SPIFault & 0x04 != 0:
        #     print('MCU Data Lost')
        # if SPIFault & 0x08 != 0:
        #     print('Double Check Error')
        # if SPIFault & 0x10 != 0:
        #     print('CRC Check Error')
        # if SPIFault & 0x20 != 0:
        #     print('Functional Security Error')
        # if SPIFault & 0x40 != 0:
        #     print('Memory Leak Check')          
        return
    def __len__(self):
        return 1

class DID0x0E16ECUInterFaultCode(udsoncan.DidCodec):
    def encode(self, val):
        return
    def decode(self, payload):
        ECUInterFault1  = struct.unpack('<3B', payload)[0]
        # if ECUInterFault1 & 0x01 !=0:
        #     print('MCU 5V over voltage')
        # if ECUInterFault1 & 0x02 !=0:
        #     print('MCU 5V under voltage')
        # if ECUInterFault1 & 0x04 !=0:
        #     print('MCU 3.3V over voltage')
        # if ECUInterFault1 & 0x08 !=0:
        #     print('MCU 3.3V under voltage')
        # if ECUInterFault1 & 0x10 !=0:
        #     print('MCU 1.8V over voltage')
        # if ECUInterFault1 & 0x20 !=0:
        #     print('MCU 1.8V under voltage')
        # if ECUInterFault1 & 0x40 !=0:
        #     print('MCU 1.0V over voltage')
        # if ECUInterFault1 & 0x80 !=0:
        #     print('MCU 1.0V under voltage')    
        # ECUInterFault2  = struct.unpack('<3B', payload)[1]
        # if ECUInterFault2 & 0x01 !=0:
        #     print('MCU 1.1V over voltage')
        # if ECUInterFault2 & 0x02 !=0:
        #     print('MCU 1.1V under voltage')
        # ECUInterFault3  = struct.unpack('<3B', payload)[2]
        # if ECUInterFault3 & 0x01 !=0:
        #     print('DDR Check Status')
        # if ECUInterFault3 & 0x02 !=0:
        #     print('EMMC Check Status')
        # if ECUInterFault3 & 0x04 !=0:
        #     print('Camera VIO Status')
        return
    def __len__(self):
        return 3

class DID0x0E15OMSFaultCode(udsoncan.DidCodec):
    def encode(self, val):
        return
    def decode(self, payload):
        OMSFault  = struct.unpack('<B', payload)[0]
        # if OMSFault & 0x01 !=0:
        #     print('Frame Order Error')
        # if OMSFault & 0x02 !=0:
        #     print('loss Frame')
        # if OMSFault & 0x04 !=0:
        #     print('Picture-Time Error')
        # if OMSFault & 0x08 !=0:
        #     print('Picture Obtain Timeout')
        # if OMSFault & 0x10 !=0:
        #     print('Picture is blocked')
        # if OMSFault & 0x20 !=0:
        #     print('Picture Blur')
        return                       # Do some stuff (reversed)
    def __len__(self):
        return 1

class DID0x0E14DMSFaultCode(udsoncan.DidCodec):
   def encode(self, val):
      return
   def decode(self, payload):
        DMSFault  = struct.unpack('<B', payload)[0]
        # if DMSFault & 0x01 !=0:
        #     print('Frame Order Error')
        # if DMSFault & 0x02 !=0:
        #     print('loss Frame')
        # if DMSFault & 0x04 !=0:
        #     print('Picture-Time Error')
        # if DMSFault & 0x08 !=0:
        #     print('Picture Obtain Timeout')
        # if DMSFault & 0x10 !=0:
        #     print('Picture is blocked')
        # if DMSFault & 0x20 !=0:
        #     print('Picture Blur')
        return                       # Do some stuff (reversed)
   def __len__(self):
      return 1

class DID0x0406DateAndTime(udsoncan.DidCodec):
    def encode(self, val):
        return
    def decode(self, payload):
        year = struct.unpack('<BBBBBB', payload)[0]
        month = struct.unpack('<BBBBBB', payload)[1]
        day = struct.unpack('<BBBBBB', payload)[2]
        hour = struct.unpack('<BBBBBB', payload)[3]
        minute = struct.unpack('<BBBBBB', payload)[4]
        second = struct.unpack('<BBBBBB', payload)[5]
        # print("Date&Time = %d-%d-%d_%d:%d:%d" %(year, month, day, hour, minute, second))
        return                       # Do some stuff (reversed)
    def __len__(self):
        return 6

class DID0x0405SysRT(udsoncan.DidCodec):
    def encode(self, val):
        return
    def decode(self, payload):
        SystemRunTime = struct.unpack('>L', payload)[0] * 0.001
        # print("SystemRunTime =%f"%SystemRunTime)
        return                      # Do some stuff (reversed)
    def __len__(self):
        return 4    # encoded paylaod is 4 byte long.

class DID0x1000BatVoltCodec(udsoncan.DidCodec):
    def encode(self, val):
        return
    def decode(self, payload):
        voltage = struct.unpack('<B', payload)[0] * 0.1
    #   print("voltage =%d"%voltage)
        return                       # Do some stuff (reversed)
    def __len__(self):
        return 1    # encoded paylaod is 4 byte long.

class DID0x310Codec(udsoncan.DidCodec):
    def encode(self, val):
        packed = struct.pack('<B', val)
        return packed 
    def decode(self, payload):
        adas_on_off  = struct.unpack('<B', payload)[0]
        # print("adas_on_off =%d"%adas_on_off)
        return                       # Do some stuff (reversed)
    def __len__(self):
        return 1    # encoded paylaod is 4 byte long.

class DID0x120codec(udsoncan.DidCodec):
    def encode(self, val):
        packet1 = struct.pack('<Q', 0x0000000000000000)
        packet2 = struct.pack('<H', 0x0000)
        packed = struct.pack('<H', val)
        packed += packet1  # decode the 32 bits value
        packed += packet2
        # print("0x0120 value = 0x%x" % val)
        return packed
    def decode(self, payload):
        val = struct.unpack('<3L', payload)[0]  # decode the 32 bits value
        # print("0x0120 value = 0x%x"%val)
        return                       # Do some stuff (reversed)
    def __len__(self):
        return 12    # encoded paylaod is 12 byte long.

class DID0x110codec(udsoncan.DidCodec):
    def encode(self, val):
        packed = struct.pack('<B', val)
        return packed
    def decode(self, payload):
        val = struct.unpack('<B', payload)[0]  # decode the 32 bits value
        # print("0x0110 value = 0x%x"%val)
        return
    def __len__(self):
        return 1    # encoded paylaod is 1 byte long.

class DID0x0100Codec(udsoncan.DidCodec):
    def encode(self, val):
        packed = struct.pack('<B', val)
        return packed 
    def decode(self, payload):
        DMS_function_on_off  = struct.unpack('<B', payload)[0]
        # if DMS_function_on_off & 0x01 != 0:
        #     print('fatigue monitoring on')
        # else:
        #     print('fatigue monitoring off')  
        # if DMS_function_on_off & 0x02 != 0:
        #     print('distraction monitoring on')
        # else:
        #     print('distraction monitoring off')    
        # if DMS_function_on_off & 0x04 != 0:
        #     print('face id on')
        # else:
        #     print('face id off')    
        # if DMS_function_on_off & 0x08 != 0:
        #     print('Driver action on')
        # else:
        #     print('Driver action off')
        return                      
    def __len__(self):
        return 1

class DID0xF184codec(udsoncan.DidCodec):
    def encode(self,val):
        year = datetime.datetime.now().strftime('%Y%m%d')[2:4]
        month=datetime.datetime.now().strftime('%Y%m%d')[4:6]
        day = datetime.datetime.now().strftime('%Y%m%d')[6:]
        date_year = int(year,16)
        date_month = int(month,16)
        date_day = int(day,16)
        packet1 = struct.pack('<B', val)
        packet2 = struct.pack('<B', date_year)
        packet3 = struct.pack('<B', date_month)
        packet4 = struct.pack('<B', date_day)
        packet5 = struct.pack('<L', 0xFFFFFFFF)
        packet6 = struct.pack('<H', 0xFFFF)
        packed = packet1 + packet2 + packet3 + packet4 + packet5 + packet6   
        return packed
    def decode(self, payload):
        val = struct.unpack('<3L', payload)[0]  # decode the 32 bits value
        return                       # Do some stuff (reversed)
    def __len__(self):
        return 10    # encoded paylaod is 8 byte long.

class DID0xF199codec(udsoncan.DidCodec):
    def encode(self,val):
        val = datetime.datetime.now().strftime('%Y%m%d')
        year_h = val[0:2]
        year_l = val[2:4]
        month = val[4:6]
        day = val[6:]
        date_year_h = int(year_h,16)
        date_year_l = int(year_l,16)
        date_month = int(month,16)
        date_day = int(day,16)
        packet1 = struct.pack('<B', date_year_h)
        packet2 = struct.pack('<B', date_year_l)
        packet3 = struct.pack('<B', date_month)
        packet4 = struct.pack('<B', date_day)
        packed =  packet1 + packet2 + packet3 + packet4
        return packed
    def decode(self, payload):
        return
    def __len__(self):
        return 4

class DID0x0E30SVNVerCodec(udsoncan.DidCodec):
    def encode(self,val):
        pass
    def decode(self, payload):
        svnversion = chr(struct.unpack('<4B', payload)[0]) + str(struct.unpack('<4B', payload)[1]) + str(struct.unpack('<4B', payload)[2]) + str(struct.unpack('<4B', payload)[3])
        return svnversion
    def __len__(self):
        return 4

class uds_client:
    def __init__(self):
        # UDS应用层客户端连接
        isotp_params = {                       # Refer to isotp documentation for full details about parameters
        'stmin' : 32,                          # Will request the sender to wait 32ms between consecutive frame. 0-127ms or 100-900ns about values from 0xF1-0xF9
        'blocksize' : 8,                       # Request the sender to send 8 consecutives frames before sending a new flow control message
        'wftmax' : 0,                          # Number of wait frame allowed before triggering an error
        'll_data_length' : 8,                  # Link layer (CAN layer) works about 8 byte payload (CAN 2.0)
        'tx_padding' : 0xaa,                   # Will pad all transmitted CAN messages about byte 0xaa. None means no padding
        'rx_flowcontrol_timeout' : 1000,       # Triggers a timeout if a flow control is awaited for more than 1000 milliseconds
        'rx_consecutive_frame_timeout' : 1000, # Triggers a timeout if a consecutive frame is awaited for more than 1000 milliseconds
        'squash_stmin_requirement' : False     # When sending, respect the stmin requirement of the receiver. If set to True, go as fast as possible.
        }
        self.config=dict(udsoncan.configs.default_client_config)
        self.config['data_identifiers'] = {
            0x0120: DID0x120codec,
            0x0110: DID0x110codec,
            0x0100: DID0x0100Codec,
            0x0310: DID0x310Codec,
            0xf187: udsoncan.AsciiCodec(14),
            0xf189: udsoncan.AsciiCodec(17),
            0xf181: udsoncan.AsciiCodec(17),
            0xf180: udsoncan.AsciiCodec(17),
            0xf17f: udsoncan.AsciiCodec(17),
            0x1000: DID0x1000BatVoltCodec,
            0x0405: DID0x0405SysRT,
            0x0406: DID0x0406DateAndTime,
            0x0E14: DID0x0E14DMSFaultCode,
            0x0E15: DID0x0E15OMSFaultCode,
            0x0E16: DID0x0E16ECUInterFaultCode,
            0x0E17: DID0x0E17SPIFaultCode,
            0x0404: DID0x0404ECUTemp,
            0x0E27: DID0x0E27J2JuncTemp,
            0xF190: udsoncan.AsciiCodec(17),
            0xF195: DID0xF195SupplierECUSoftwareVer,
            0x0E30: DID0x0E30SVNVerCodec,
            0xf18E: udsoncan.AsciiCodec(14),
            0xf197: udsoncan.AsciiCodec(20),
            0xF184: DID0xF184codec,
            0xF199: DID0xF199codec
        }
        tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=0x722, rxid=0x7a2) # Network layer addressing scheme
        global bus0
        stack = isotp.CanStack(bus=bus0, address=tp_addr, params=isotp_params)              # Network/Transport layer (IsoTP protocol)
        self.conn = PythonIsoTpConnection(stack)                                            # interface between Application and Transport layer
        self.client = Client(self.conn, request_timeout=2, config=self.config)
    def client_connect(self):
        return Client(self.conn, request_timeout=2, config=self.config)                     # Application layer (UDS protocol)
    def DSTCX_1(self):
        '''测试第一步 85 01 控制 DTC 设置开启
        '''
        with self.client as client:
            try:
                client.change_session(0x03)
                client.control_dtc_setting(setting_type=0x01)
                test_logger.info('设置85 01')
                read_data_0120 = client.read_data_by_identifier(0x0120)
                read_data_0110 = client.read_data_by_identifier(0x0110)
                if read_data_0110.data.hex() != '011001':
                    client.change_session(0x03)
                    uds_client().DSTX_write_data(0x0110, 0x01)
                    client.read_data_by_identifier(0x0110)
                test_logger.info('ECU处于非工厂模式')
                if '0120ffff' not in read_data_0120.data.hex():
                    test_logger.error('DID 0120 对应数据不是ff, dtc未全部使能')
                else:
                    test_logger.error('dtc全部使能')
            except:
                test_logger.error('初始化测试环境失败')
            try:
                client.change_session(3)
                request_seed = client.request_seed(1)
                send_key = client.send_key(level = 2, key = SecureAlgo(seed = request_seed.service_data.seed , level = 1))
                client.change_session(1)
                test_logger.info("处于安全访问状态")
            except:
                test_logger.error("未处于安全访问状态")
                
    def DSTCX_clear_dtc(self):
        '''clear DTC
        '''
        with self.client as client:
            try:
                client.clear_dtc()
                print('Pass! DTCs are cleared')
            except:
                print('Fail! DTCs are not cleared')
    def DSTCX_get_dtc_num(self,status_mask):
        ''' 19 01服务
        '''
        with self.client as client:
            responce_dtc_num_get = client.get_number_of_dtc_by_status_mask(status_mask)
            dtc_num = responce_dtc_num_get.data.hex()[4:]
            return dtc_num

    def DSTCX_get_dtc(self, dtc_str, check_status):
        '''19 02 
        '''
        with self.client as client:
            responce_dtc_get = client.get_dtc_by_status_mask(status_mask=0x09)  # 获取dtc内容
            dtc_num = int((len(responce_dtc_get.data.hex())-4)/8)
            flag = 0
            for i in range(dtc_num):
                dtc_status_str = responce_dtc_get.data.hex()[4+i*8:12+i*8]
                print(dtc_status_str)
                if dtc_str in dtc_status_str:
                    dtc_status = dtc_status_str[-2:]
                    dtc_status = int(dtc_status, 16)
                    if dtc_status & check_status == check_status:
                        flag = 1
                        break
        return flag  # 读到dtc，flag置为1

    def DSTCX_get_dtc_0A(self, dtc_str, check_status):
        '''19 02 0A
        '''
        with self.client as client:
            responce_dtc_get = client.get_dtc_by_status_mask(status_mask=0x0A)  # 获取dtc内容
            dtc_num = int((len(responce_dtc_get.data.hex())-4)/8)
            flag = 0
            for i in range(dtc_num):
                dtc_status_str = responce_dtc_get.data.hex()[4+i*8:12+i*8]
                print(dtc_status_str)
                if dtc_str in dtc_status_str:
                    dtc_status = dtc_status_str[-2:]
                    dtc_status = int(dtc_status, 16)
                    if dtc_status & check_status == check_status:
                        flag = 1
                        break
        return flag  # 读到dtc，flag置为1

    def DSTCX_get_snapshot(self, dtc): 
        '''19 04
        ''' 
        with self.client as client:
            dtc_snapshot = client.get_dtc_snapshot_by_dtc_number(dtc,0xff)
            status = dtc_snapshot.service_data.dtcs[0].status.get_byte().hex()
            if status == '00' and len(dtc_snapshot.data.hex()) == 10:
                flag = 1
            else:
                flag = 0
        return flag

    def DSTCX_get_dtc_extended(self,dtc):
        '''19 06
        '''
        with self.client as client:
            dtc_extended_data = client.get_dtc_extended_data_by_dtc_number(dtc,0xff,data_size=5)
            dtc_extended_hex_data = dtc_extended_data.service_data.dtcs[0].status.get_byte().hex()
            if dtc_extended_hex_data == '00' and len(dtc_extended_data.data.hex()) == 10:
                    flag = 1
            else:
                    flag = 0
        return flag

    def DSTCX_dtc_enable(self,hex):
        '''01 20
        '''
        with self.client as client:
            client.write_data_by_identifier(0x0120, hex)
    
    def DSTCX_change_session(self, session):
        """10
        """
        with self.client as client:
            change_session = client.change_session(session)
        return change_session

    def DSTCX_control_dtc_setting(self, setting_type):
        """85
        """
        with self.client as client:
            client.control_dtc_setting(setting_type)

    def DSTCX_ecu_reset(self, reset_type):
        """11
        """
        with self.client as client:
            client.ecu_reset(reset_type)
    
    def DSTCX_request_seed(self, seed):
        """27 01
        """
        with self.client as client:
            request_seed = client.request_seed(seed)
        return request_seed

    def DSTCX_send_key(self, level, key):
        """27 02
        """
        with self.client as client:
            send_key = client.send_key(level, key)
        return send_key

    def DSTX_read_data(self, did):
        """读DID
        """
        with self.client as client:
            read_data = client.read_data_by_identifier(did)
        return read_data

    def DSTX_write_data(self, did, value):
        """写DID
        """
        with self.client as client:
            write_data = client.write_data_by_identifier(did,value)
        return write_data

    def DSTX_communication_control(self, control_type, communication_type):
        """网络管理
        """
        with self.client as client:
            communication_control = client.communication_control(control_type, communication_type)
        return communication_control