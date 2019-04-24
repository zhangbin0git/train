#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# @Time    : 2019-04-03 1:18
# @Author  : Zhang Bin
# @Site    : 
# @File    : jnjt_oa.py
# @Software: PyCharm

import mechanize
import sys

# 设置编码
# reload(sys)
# sys.setdefaultencoding('utf8')

class JnjtOa_post:
    """连接集团oa系统，填报表单"""
    def __init__(self, http):
        self.http = http
        self.web_browser = mechanize.Browser()


    def open_web(self):
        self.web_browser.open(self.http)
        # self.web_browser.set_handle_robots(False)
        # self.web_browser.set_handle_equiv(False)
        # print self.web_browser.response().read()

        self.web_browser.addheaders = [('User-agent',
                          'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.11) Gecko/20100701 Firefox/3.5.11')]  ##模拟浏览器头
        ###设置一些参数，因为是模拟客户端请求，所以要支持客户端的一些常用功能，比如gzip,referer等
        self.web_browser.set_handle_equiv(True)
        self.web_browser.set_handle_gzip(True)
        self.web_browser.set_handle_redirect(True)
        self.web_browser.set_handle_referer(True)
        self.web_browser.set_handle_robots(False)

        self.web_browser.set_handle_refresh(
            mechanize._http.HTTPRefreshProcessor(), max_time=1)

        ###这个是degbug##你可以看到他中间的执行过程，对你调试代码有帮助
        self.web_browser.set_debug_http(True)
        # self.web_browser.set_debug_redirects(True)
        # self.web_browser.set_debug_responses(True)

    def read_form(self):
        mid = self.web_browser.forms()
        for i in mid:
            print i

    def sub_form(self):
        # 填写表单
        self.web_browser.select_form(nr=0)
        self.web_browser['userName'] = 'sys'
        self.web_browser['password'] = '1234'
        # self.web_browser['org_no']= ['']
        print self.web_browser['org_no']

        # mid_pots = self.web_browser.submit()
        # self.web_browser.open('http://10.1.3.33:7001/Liems/xslt/index.jsp')
        # print self.web_browser.response().read()
        # for i in mid_pots:
        #     print i
        print self.web_browser.response().read()


    def other_mothet(self):
        for link in self.web_browser.links():
            print link.url + ':' + link.text
        # new_link = elf.web_browser.click_link(text='')
        # self.web_browser.open(new_link)
        # print self.web_browser.response().read()

    def web_main(self):
        self.open_web()
        self.read_form()
        self.sub_form()

http = "http://10.1.3.33:7001/Liems/"
oa = JnjtOa_post(http)
oa.open_web()
oa.read_form()
oa.sub_form()
# oa.other_mothet()
