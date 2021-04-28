#!/usr/bin/python
import re
if __name__=='__main__':
    t=re.search('\.(\s)','www.runoob. com')
    print t.group()