#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019-4-3 18:23 
# @Author : Mark 
# @Site : office
# @File : selenium_chrome_post.py 
# @Software: PyCharm Community Edition
# 接口对接协议的密码和开发人有关
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email import utils
import smtplib
import json
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import datetime
import time

# 相关参数
url = r"http://10.1.3.33:7001/Liems/"
api_url = r"http://10.35.1.21/interface-platform-web/invoke/bloc_getElecPq.do"
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
        """前台开启浏览器模式"""
        # 返回为打开的浏览器实体，path：chrome插件地址
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

    def gen_para(self, startdate, enddate, clientKey="d1885d575a7211e988f500e066efe6e6", serviceKey="bloc_getElecPq"):
        """生产客户端请求json，数据。包括起止时间"""
        parameter = \
            {"clientKey":clientKey,
            "params":{"startDate":startdate, "endDate":enddate},
            "serviceKey":serviceKey}
        return parameter

    def get_data(self, api_url):
        """从售电API端口提取数据"""
        # 获取昨天日期
        yesterday = datetime.date.today() + datetime.timedelta(-1)
        # 格式化成2018-01-01形式
        startdate = yesterday.strftime("%Y-%m-%d")
        enddate = yesterday.strftime("%Y-%m-%d")
        # 生产请求参数
        req = self.gen_para(startdate, enddate)
        # 指定json.dumps生成的字符串之后,可以直接发送数据而不进行URL编码
        # 需要明确指定Content-Tpye
        response = requests.post(api_url, json.dumps(req),
                                 headers={'Content-Type': 'application/json'})
        return response.json()

    def post_data(self, tab0_text2, tab0_text3, tab0_text4, tab0_text5):
        """上报数据"""
        # 点击"数据上报"按钮
        self.driver.find_element_by_xpath("//div[contains(text(), "
                                          "'数据上报')]").click()
        # 等待页面加载
        time.sleep(2)
        # 点击"晋能售电公司售电日报"按钮
        self.driver.find_element_by_xpath("//label[contains(text(), "
                                           "'售电日报')]").click()
        # 等待页面加载
        time.sleep(2)
        # 由于网站使用frame框架，切换frame
        self.driver.switch_to_frame("mainFrame")
        # 点击"新建"按钮
        self.driver.find_element_by_id("New").click()
        # 等待页面加载
        time.sleep(2)
        # 填入数据
        self.driver.find_element_by_id("tab0_text2").send_keys(tab0_text2)
        self.driver.find_element_by_id("tab0_text3").send_keys(tab0_text3)
        self.driver.find_element_by_id("tab0_text4").send_keys(tab0_text4)
        self.driver.find_element_by_id("tab0_text5").send_keys(tab0_text5)
        # 点击"保存"按钮
        self.driver.find_element_by_id("Save").click()
        # 等待页面加载
        time.sleep(2)
        # 点击所有操作按钮
        self.driver.find_element_by_id("taskDetail").click()
        # 点击"提交"按钮
        self.driver.find_element_by_class_name("wf_mouseout").click()
        self.driver.close()
        return "200"

    def feedback(self):
        """效验上报情况，反馈"""
        pass

    def send_email(self, from_addr, password, to_addr, smtp_server):
        """对上报情况通过email通知用户"""
        from_addr = from_addr
        password = password
        to_addr = to_addr
        smtp_server = smtp_server
        # 发送相关信息，应html的格式展示
        msg = MIMEText('<html><body><h1>上报正常</h1>' +
            '<p>send by administrator</p>' + '</body></html>', 'html', 'utf-8')
        msg['From'] = self._format_addr(u'生产日报自动上报客户端 <%s>' % from_addr)
        msg['To'] = self._format_addr(u'管理员 <%s>' % to_addr)
        msg['Subject'] = Header(u'生产日报自动上报情况', 'utf-8').encode()
        # 服务器配置
        server = smtplib.SMTP(smtp_server, 25)
        # 打印出和SMTP服务器交互的所有信息
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

    def close_windows(self):
        """关闭所有窗口"""
        self.driver.quit()

    def _format_addr(self, s):
        # 来格式化一个邮件地址
        name, addr = utils.parseaddr(s)
        return utils.formataddr(
            (Header(name, 'utf-8').encode(),
             addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    def run(self):
        """整体封装运行"""
        # 打开界面，登录系统
        self.operation_auth(url, username, password)
        # 从售电API端口提取数据
        # 上报数据
        self.post_data(tab0_text2, tab0_text3, tab0_text4, tab0_text5)
        # 效验上报情况，反馈
        # 对上报情况通过email通知用户
        # 关闭所有窗口
        self.close_windows()
        # 整体封装运行





web_post = WebPost(path)
# web_post.operation_auth(url, username, password)
# web_post.close_windows()
response = web_post.get_data(api_url)
print(response)
