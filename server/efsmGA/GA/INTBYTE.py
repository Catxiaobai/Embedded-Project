# encoding:utf-8
import random
class INTBYTE(object):
    def __init__(self):
        self.name=""
    def NAME(self,str):
        self.name=str
    def read(self):
        print self.name
        return self.name
    def INT8(self,l=0,r=255):
        return random.randint(l, r)

    def INT16(self,l=0,r=65535):
        return random.randint(l, r)

    def INT32(self,l=0,r=4294967295):
        return random.randint(l, r)

    def INT64(self,l=0,r=18446744073709551615):
        return random.randint(l, r)

    def IntByte_Random(self,l=0,r=0):
        if self.name=="INT8":
            if r!=0:
                return self.INT8(l,r)
            else:
                return self.INT8()
        elif self.name=="INT16":
            if r!=0:
                return self.INT16(l,r)
            else:
                return self.INT16()
        elif self.name=="INT32":
            if r!=0:
                return self.INT32(l,r)
            else:
                return self.INT32()
        elif self.name=="INT64":
            if r!=0:
                return self.INT64(l,r)
            else:
                return self.INT64()

if __name__ == '__main__':
    protocol1=INTBYTE()
    protocol1.NAME("INT8")
    protocol1.read()
    print protocol1.IntByte_Random()