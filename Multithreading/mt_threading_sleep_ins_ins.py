#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019-5-8 11:36 
# @Author : Mark 
# @Site :  
# @File : mt_threading_sleep_ins_ins.py 
# @Software: PyCharm Community Edition

# 创建Thread的实例，传给它一个可调用的类实例


import threading
from time import sleep, ctime

loops = [4, 2]

class ThreadFunc(object):
    def __init__(self, func, args, name=''):
        self.name = name
        self.func = func
        self.args = args

    # Python给类提供了名为__call__的特别方法，该方法允许程序员创建可调用的对象(实例)。
    # 默认情况下，__call__方法是没有实现的，这意味着大多数情况下实例是不可调用的。
    def __call__(self):
        self.func(*self.args)

def loop(nloop, nsec):
    print('start loop', nloop, 'at:', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at:', ctime())

def main():
    print('starting at:', ctime())
    threads = []
    nloops = list(range(len(loops)))

    for i in nloops:        # create all threads
        t = threading.Thread(
            target=ThreadFunc(loop, (i, loops[i]),
            loop.__name__))
        threads.append(t)

    for i in nloops:        # start all threads
        threads[i].start()

    for i in nloops:        # wait for completion
        threads[i].join()

    print('all DONE at:', ctime())

if __name__ == '__main__':
    main()
