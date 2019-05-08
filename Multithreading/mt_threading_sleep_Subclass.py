#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019-5-8 17:13 
# @Author : Mark 
# @Site :  
# @File : mt_threading_sleep_Subclass.py 
# @Software: PyCharm Community Edition

#派生Thread的子类，并创建子类的实例

import threading
from time import sleep, ctime

loops = [4, 2]

class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        # 调用基类的构造函数
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
    # 这里必须要写run函数
    def run(self):
        self.func(*self.args)

def loop(nloop, nsec):
    print('start loop ' + str(nloop) + ' at: ' + str(ctime()))
    sleep(nsec)
    print('loop ' + str(nloop) + ' done at: ' + str(ctime()))

def main():
    print('starting at:', ctime())
    threads = []
    nloops = list(range(len(loops)))

    for i in nloops:
        t = MyThread(loop, (i, loops[i]),
            loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('all DONE at:', ctime())

if __name__ == '__main__':
    main()
