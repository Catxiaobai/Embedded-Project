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
        self.message = []
        self.crc16=0
        fo = open(filePath, 'r')
        self.format = json.load(fo)
        fo.close()
        #self.fhead=int(self.format[0]['value'])
        #self.fend=int(self.format[len(self.format)-1]['value'])
        self.IntDateGeneration=INTBYTE.INTBYTE()
    def set(self,message):
        self.message=[]
        for i in self.format:
            name=i['name']
            data=0
            if name=="fhead" or name=="fend":
                data=int(i['value'][0])
            if message.has_key(name):
                data=message[name]
            if data==None:
                data=0
            self.message.append(data)
        self.crc16 = self.getCrc()
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
        ans=[]
        ans.extend(self.message)
        ans.insert(-1,self.crc16)
        return ans
    def dateGeneration(self,name):#dataGeneration
        tmp=None
        for i in self.format:
            if i['name']==name:
                tmp=i
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
            return int(random.choice(value))
    def getDataType(self,name):
        for i in self.format:
            if i['name'] == name:
                return i['type']

    def readBadHead(self, badhead=0):
        ans = []
        ans.extend(self.message)
        ans[0]=badhead
        ans.insert(-1, self.crc16)
        return ans

    def readBadEnd(self, badend=0):
        ans=[]
        ans.extend(self.message)
        ans[-1] = badend
        ans.insert(-1, self.crc16)
        return ans

    def readBadCrc(self, badcrc=0):
        ans = []
        ans.extend(self.message)
        ans.insert(-1, badcrc)
        return ans
if __name__ == '__main__':
    protocol1=protocol()
    protocol1.set({})
    print protocol1.getCrc()
    print protocol1.read()
    print protocol1.getDataType("data")
    print protocol1.readBadEnd(77)
    print protocol1.readBadHead(88)
    print protocol1.readBadCrc(90)
