#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019-5-8 17:30 
# @Author : Mark 
# @Site :  
# @File : my_thread.py 
# @Software: PyCharm Community Edition


# 建立独立模块，通过派生Thread的子类，并创建子类的实例
import threading
from time import time, ctime

class my_thread(threading.Thread):
    def __init__(self, func, args, name='', verb=False):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.verb = verb

    def get_result(self):
        return self.res

    def run(self):
        print('starting', self.name, 'at:', ctime())
        self.res = self.func(*self.args)
        print(self.name, 'finished at:', ctime())
