#-*- coding: utf-8
from decimal import Decimal
import json
import INTBYTE
import random
import struct



filepath = './efsmGA/files/'
def dTob(n, pre=4):
    '''
    把一个带小数的十进制数n转换成二进制
    小数点后面保留pre位小数
    '''
    string_number1 = str(n) #number1 表示十进制数，number2表示二进制数
    flag = False
    for i in string_number1: #判断是否含小数部分
        if i == '.':
            flag = True
            break
    if flag:
        string_integer, string_decimal = string_number1.split('.') #分离整数部分和小数部分
        integer = int(string_integer)
        decimal = Decimal(str(n)) - integer
        l1 = [0,1]
        l2 = []
        decimal_convert = ""
        while True:
           if integer == 0: break
           x,y = divmod(integer, 2)  #x为商，y为余数
           l2.append(y)
           integer = x
        string_integer = ''.join([str(j) for j in l2[::-1]])  #整数部分转换成二进制
        i = 0
        while decimal != 0 and i < pre:
            result = int(decimal * 2)
            decimal = decimal * 2 - result
            decimal_convert = decimal_convert + str(result)
            i = i + 1
        string_number2 = string_integer + '.' + decimal_convert
        return float(string_number2)
    else: #若十进制只有整数部分
        l1 = [0,1]
        l2 = []
        while True:
           if n == 0: break
           x,y = divmod(n, 2)  #x为商，y为余数
           l2.append(y)
           n = x
        string_number = ''.join([str(j) for j in l2[::-1]])
        return int(string_number)
class CRC():
    def __init__(self, info, crc_n=32):
        self.info = info
        loc=[]
        if crc_n == 8:
            loc = [8, 2, 1, 0]
        elif crc_n == 32:
            loc = [32, 26, 23, 22, 16, 12, 11, 10, 8, 7, 5, 2, 1, 0]
        elif crc_n == 16:
            loc = [16, 15, 2, 0]
        elif crc_n == 4:
            loc = [4, 3, 0]
        p = [0 for i in range(crc_n + 1)]
        for i in loc:
            p[i] = 1
        p = p[::-1]
        info = self.info[:]
        times = len(info)
        n = crc_n + 1
        for i in range(crc_n):
            info.append(0)
        q = []
        for i in range(times):
            if info[i] == 1:
                q.append(1)
                for j in range(n):
                    info[j + i] = info[j + i] ^ p[j]
            else:
                q.append(0)
        check_code = info[-crc_n::]
        code = self.info[:]
        for i in check_code:
            code.append(i)
        self.crc_n = crc_n
        self.p = p
        self.q = q
        self.check_code = check_code
        self.code = code
class protocol:
    def __init__(self,filePath=filepath+'format.txt'):
        self.result = []
        self.message = []
        self.crc16=0
        fo = open(filePath, 'r')
        self.format = json.load(fo)
        fo.close()
        #self.fhead=int(self.format[0]['value'])
        #self.fend=int(self.format[len(self.format)-1]['value'])
        self.IntDateGeneration=INTBYTE.INTBYTE()

    def set(self,data):
        self.result = []
        ans={}
        for key,value in data.items():
            key=key.split('_')
            data_protocol=key[0]
            if ans.has_key(data_protocol):
                ans[data_protocol][key[1]]=value
            else:
                ans[data_protocol]={}
                ans[data_protocol][key[1]]=value
        for key,message in ans.items():
            protocol_object=self.format[key]
            self.message = []
            for i in protocol_object:
                name=i['name']
                dt=0
                if name=="fhead" or name=="fend":
                    dt=int(i['value'][0])
                if message.has_key(name):
                    dt=message[name]
                if data==None:
                    dt=0
                self.message.append(dt)
            self.crc16 = self.getCrc()
            message_tmp=[]
            k=0
            for i in protocol_object:
                if int(i['length'])==2:
                    str1 = ""
                    if type(self.message[k])==type(0.1):
                        floatStr=str(self.message[k])
                        indexe=floatStr.find('e')
                        if indexe>0:
                            floatStr=floatStr[:indexe]
                        floatStr=floatStr.split('.')
                        for i in floatStr:
                            str1=str1+i
                        str1=int(str1)
                    else:
                        str1=self.message[k]
                    str1='0x{:04x}'.format(str1)
                elif int(i['length'])==1:
                    str1 = ""
                    if type(self.message[k]) == type(0.1):
                        floatStr = str(self.message[k])
                        indexe = floatStr.find('e')
                        if indexe > 0:
                            floatStr = floatStr[:indexe]
                        floatStr = floatStr.split('.')
                        for i in floatStr:
                            str1 = str1 + i
                        str1 = int(str1)
                    else:
                        str1 = self.message[k]
                    str1='0x{:02x}'.format(self.message[k])
                elif int(i['length'])==3:
                    str1 = ""
                    if type(self.message[k]) == type(0.1):
                        floatStr = str(self.message[k])
                        indexe = floatStr.find('e')
                        if indexe > 0:
                            floatStr = floatStr[:indexe]
                        floatStr = floatStr.split('.')
                        for i in floatStr:
                            str1 = str1 + i
                        str1 = int(str1)
                    else:
                        str1 = self.message[k]
                    str1='0x{:06x}'.format(self.message[k])
                elif int(i['length'])==4:
                    str1 = ""
                    if type(self.message[k]) == type(0.1):
                        floatStr = str(self.message[k])
                        indexe = floatStr.find('e')
                        if indexe > 0:
                            floatStr = floatStr[:indexe]
                        floatStr = floatStr.split('.')
                        for i in floatStr:
                            str1 = str1 + i
                        str1 = int(str1)
                    else:
                        str1 = self.message[k]
                    str1='0x{:08x}'.format(self.message[k])
                elif int(i['length'])==5:
                    str1 = ""
                    if type(self.message[k]) == type(0.1):
                        floatStr = str(self.message[k])
                        indexe = floatStr.find('e')
                        if indexe > 0:
                            floatStr = floatStr[:indexe]
                        floatStr = floatStr.split('.')
                        for i in floatStr:
                            str1 = str1 + i
                        str1 = int(str1)
                    else:
                        str1 = self.message[k]
                    str1='0x{:10x}'.format(self.message[k])
                k+=1
                message_tmp.append(str1[:])
            self.message.insert(-1, self.crc16)
            message_tmp.insert(-1, '0x{:04x}'.format(self.crc16))
            self.result.append(message_tmp)
    def getCrc(self,crcnum=16):
        binstr=""
        for i in self.message:
            if type(i)==type(0.1):
                floatBitStr=str(dTob(i))
                indexe=floatBitStr.find('e')
                if indexe>0:
                    floatBitStr=floatBitStr[:indexe]
                floatBitStr=floatBitStr.split('.')
                for i in floatBitStr:
                    binstr=binstr+i
            elif type(i)==type(1):
                binstr=binstr+str(bin(i))[2:]
        m = []
        for i in range(len(binstr)):
            m.append(int(binstr[i]))
        crc =CRC(m,crcnum)
        jyh=crc.check_code
        jyh1 = ''
        for i in jyh:
            jyh1 += str(i)
        jyh1 = int(jyh1, 2)
        return jyh1
    def read(self):
        return self.result
    def dateGeneration(self,name):#dataGeneration
        tmp=None
        name = name.split('_')
        for i in self.format[name[0]]:
            if i['name'] == name[1]:
                tmp = i
                break
        type=tmp["type"]
        if "INT" in type:
            l=int(tmp['lower_bound'])
            r=int(tmp['upper_bound'])
            self.IntDateGeneration.NAME(type)
            return self.IntDateGeneration.IntByte_Random(l,r)
        if "FLOAT" in type:
            l=float(tmp['lower_bound'])
            r=float(tmp['upper_bound'])
            self.IntDateGeneration.NAME(type)
            return self.IntDateGeneration.IntByte_Random(l,r)
        elif "ENUM" in type:
            value=tmp['value']
            data_str=str(random.choice(value))
            if '0x' in data_str:
                return int(data_str, 16)
            else:
                return int(data_str)
    def getDataType(self,name):
        name=name.split('_')
        for i in self.format[name[0]]:
            if i['name'] == name[1]:
                return i['type']

    def readBadHead(self, badhead=0):
        ans = []
        for i in self.result:
            message_tmp=i[:]
            message_tmp[0]='0x{:04x}'.format(badhead)
            ans.append(message_tmp[:])
        return ans

    def readBadEnd(self, badend=0):
        ans = []
        for i in self.result:
            message_tmp = i[:]
            message_tmp[0] = '0x{:04x}'.format(badend)
            ans.append(message_tmp)
        return ans

    def readBadCrc(self, badcrc=0):
        ans = []
        for i in self.result:
            message_tmp = i[:]
            message_tmp[0] = '0x{:04x}'.format(badcrc)
            ans.append(message_tmp[:])
        return ans

if __name__ == '__main__':
    protocol1 = protocol()
    protocol1.set({"RS232_ctr": 257,"RS232_data":0})
    print protocol1.read()
    print protocol1.readBadEnd(77)
    print protocol1.readBadHead(88)
    print protocol1.readBadCrc(90)

