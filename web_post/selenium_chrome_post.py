#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019-4-3 18:23 
# @Author : Mark 
# @Site : office
# @File : selenium_chrome_post.py 
# @Software: PyCharm Community Edition
# 接口对接协议的密码和开发人有关

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import time
url = r"http://10.1.3.33:7001/Liems/"
username = r"JNDLLLSD"
password = r"1234"
path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

class WebPost():
    """通过从售电公司api端口提取当日售电量数据，
    自动登录晋能电力集团生产管理信息系统上报当日售电量"""
    def __init__(self, path):
        # 必要参数path：chrome插件地址
        self.path = path

    def open_chrome(self, path):
        # # 前台开启浏览器模式,返回为打开的浏览器实体，path：chrome插件地址
        driver = webdriver.Chrome(path)
        return driver

    def operation_auth(self, url, username, password):
        """用户授权登录"""
        # 打开指定的网址
        self.driver = self.open_chrome(self.path)
        self.driver.get(url)
        # 找到输入框
        sys_user = self.driver.find_element_by_id("userName")
        # 输入指定内容
        sys_user.send_keys(username)
        sys_pwd = self.driver.find_element_by_id("password")
        sys_pwd.send_keys(password)
        # 提交表单，查找提交按钮并点击
        self.driver.find_element_by_class_name("login_btn").click()

    def close_windows(self):
        """关闭窗口"""
        self.driver.quit()
    def send_email(self,user_email):
        """将上报情况以email形式发送给用户"""

web_post = WebPost(path)
web_post.operation_auth(url, username, password)
web_post.close_windows()
