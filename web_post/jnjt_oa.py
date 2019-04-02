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
reload(sys)
sys.setdefaultencoding('utf8')

class JnjtOa_post:
    """连接集团oa系统，填报表单"""
    def __init__(self, http):
        self.http = http
        self.web_browser = mechanize.Browser()


    def open_web(self):
        self.web_browser.open(self.http)
        # self.web_browser.set_handle_robots(False)
        # self.web_browser.set_handle_equiv(False)
        # self.web_browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686;'
        #  'en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        # print self.web_browser.response().read()

    def read_form(self):
        mid = self.web_browser.forms()
        for i in mid:
            print i

    def sub_form(self):
        # 填写表单
        self.web_browser.select_form(nr=0)
        self.web_browser['userName'] = 'JNDLLIUCHENGLIANG'
        self.web_browser['password'] = '1234'
        self.web_browser.submit()
        # print self.web_browser.response().read()


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

http = "http://202.99.219.114:8888/Liems/"
oa = JnjtOa_post(http)
oa.open_web()
oa.read_form()
oa.sub_form()
oa.other_mothet()
