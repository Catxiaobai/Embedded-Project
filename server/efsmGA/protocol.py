import json
import INTBYTE
import random

filepath = './efsmGA/files/'
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
        self.fhead=int(self.format[0]['upper_bound'])
        self.fend=int(self.format[len(self.format)-1]['upper_bound'])
        self.IntDateGeneration=INTBYTE.INTBYTE()
    def set(self,message):
        self.message=[]
        for i in self.format[1:len(self.format)-1]:
            name=i['name']
            data=None
            if message.has_key(name):
                data=message[name]
            self.message.append(data)
        self.crc16 = self.getCrc()
    def getCrc(self,crcnum=16):
        binstr=str(bin(int(self.fhead)))[2:]
        for i in self.message:
            if i!=None:
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
        ans.append(self.fhead)
        ans.extend(self.message)
        ans.append(self.crc16)
        ans.append(self.fend)
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
        elif "enum" in type:
            value=tmp['value']
            return int(random.choice(value))
    def getDataType(self,name):
        for i in self.format:
            if i['name'] == name:
                return i['type']
if __name__ == '__main__':
    protocol1=protocol()
    protocol1.set([23,123])
    print protocol1.getCrc()
    print protocol1.read()
    print protocol1.getDataType("data")
    #protocol1.readBadEnd(77)
    #protocol1.readBadHead(88)
    #protocol1.readBadCrc(90)
