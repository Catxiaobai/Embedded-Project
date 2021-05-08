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
    def __init__(self):
        self.fhead="00055"
        self.message = []
        self.crc16=""
        self.fend="00066"
    def set(self,message):
        self.message = []
        for i in message:
            j=str(i)
            num=5-len(j)
            for k in range(num):
                j='0'+j
            self.message.append(j)
        self.crc16 = self.getCrc()
    def getCrc(self,crcnum=16):
        binstr=str(bin(int(self.fhead)))[2:]
        for i in self.message:
            binstr=binstr+str(bin(int(i)))[2:]
        m = []
        for i in range(len(binstr)):
            m.append(int(binstr[i]))
        crc =CRC(m,crcnum)
        jyh=crc.check_code
        jyh1 = ''
        for i in jyh:
            jyh1 += str(i)
        jyh1 = str(int(jyh1, 2))
        if len(jyh1) < 5:
            for i in range(5 - len(jyh1)):
                jyh1 = '0' + jyh1
        return jyh1
    def read(self):
        ans=self.fhead
        for i in self.message:
            ans+=i
        ans+=self.crc16+self.fend
        return ans
    def readBadHead(self,badhead=0):
        badheadstr=str(badhead)
        num = 5 - len(badheadstr)
        for k in range(num):
            badheadstr = '0' + badheadstr
        ans = badheadstr
        for i in self.message:
            ans += i
        ans += self.crc16 + self.fend
        return ans
    def readBadEnd(self,badend=0):
        badendstr=str(badend)
        num = 5 - len(badendstr)
        for k in range(num):
            badendstr = '0' + badendstr
        ans = self.fhead
        for i in self.message:
            ans += i
        ans += self.crc16 + badendstr
        return ans
    def readBadCrc(self,badcrc=0):
        badendcrc=str(badcrc)
        num = 5 - len(badendcrc)
        for k in range(num):
            badendcrc = '0' + badendcrc
        ans = self.fhead
        for i in self.message:
            ans += i
        ans += badendcrc+self.fend
        return ans
if __name__ == '__main__':
    protocol1=protocol()
    protocol1.set([11123,123])
    protocol1.read()
    protocol1.readBadEnd(77)
    protocol1.readBadHead(88)
    protocol1.readBadCrc(90)
