#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019-5-8 11:18 
# @Author : Mark 
# @Site :  
# @File : mt_threading_sleep_ins_para.py 
# @Software: PyCharm Community Edition

# 多线程，使用创建Thread实例，传递一个参数给他

import threading
from time import sleep, ctime

loops = [4, 2]

def loop(nloop, nsec):
    print('start loop', nloop, 'at:', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at:', ctime())

def main():
    print('starting at:', ctime())
    threads = []
    nloops = list(range(len(loops)))

    for i in nloops:
        # 创建thread的实例，传递参数
        t = threading.Thread(target=loop, args=(i, loops[i]))
        threads.append(t)

    for i in nloops:            # start threads
        threads[i].start()

    for i in nloops:            # wait for all
        # join方法只有在你需要等待线程完成的时候才有用
        threads[i].join()       # threads to finish

    print('all DONE at:', ctime())

if __name__ == '__main__':
    main()
