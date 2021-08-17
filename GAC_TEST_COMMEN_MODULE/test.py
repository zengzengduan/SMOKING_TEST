import struct
payload = b'\x22\x02\x03\x04'
print(type(payload))
print(len(payload))
# svnversion = chr(struct.unpack('<4B', payload)[0]) + str(struct.unpack('<4B', payload)[1]) + str(struct.unpack('<4B', payload)[2]) + str(struct.unpack('<4B', payload)[3])
# print(svnversion)
