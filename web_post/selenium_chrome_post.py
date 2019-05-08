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

def read_config(filename):
    """读取配置文件, status_code状态，为1表示成功,0表示失败,value为返回对象"""
    # status_code为1表示成功,0表示失败
    ret = {'status_code':1, 'value':{}}
    try:
        with open(filename, 'r') as f:
            for line in f.readlines():
                (key, value) = line.strip().split('=')
                ret['value'][key.strip()] = value.strip()
    except:
        ret['status_code'] = 0
    return ret


class WebPost():
    """通过从售电公司api端口提取当日售电量数据，
    自动登录晋能电力集团生产管理信息系统上报当日售电量"""
    def __init__(self, path, api_url, url, username, password, from_addr,
                 email_password, to_addr, smtp_server):
        # 必要参数path：chrome插件地址, api_url:api接口地址
        # url上传数据web地址，username、password上传web账号密码
        # status为各个函数的专题情况，1为正常，0为失败
        self.path = path
        self.api_url = api_url
        self.url = url
        self.username = username
        self.password = password
        self.from_addr = from_addr
        self.email_password = email_password
        self.to_addr = to_addr
        self.smtp_server = smtp_server
        self.status = {}

    def open_chrome(self, path):
        """前台开启浏览器模式"""
        # 返回为打开的浏览器实体，path：chrome插件地址
        try:
            driver = webdriver.Chrome(path)
            self.status['open_chrome'] = 1
            return driver
        except:
            self.status['open_chrome'] = 0

    def operation_auth(self, url, username, password):
        """用户授权登录"""
        try:
            # 打开指定的网址
            self.driver = self.open_chrome(self.path)
            if self.status['open_chrome'] == 1:
                self.driver.get(url)
                # 找到输入框
                sys_user = self.driver.find_element_by_id("userName")
                # 输入指定内容
                sys_user.send_keys(username)
                sys_pwd = self.driver.find_element_by_id("password")
                sys_pwd.send_keys(password)
                # 提交表单，查找提交按钮并点击
                self.driver.find_element_by_class_name("login_btn").click()
                self.status['operation_auth'] = 1
            else:
                self.status['operation_auth'] = 0
                print("开启浏览器模式失败！")

        except:
            self.status['operation_auth'] = 0

    def gen_para(self, startdate, enddate,
                 clientKey="d1885d575a7211e988f500e066efe6e6",
                 serviceKey="bloc_getElecPq"):
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
        try:
            response = requests.post(
                api_url, json.dumps(req),
                headers={'Content-Type': 'application/json'})
            self.status['get_data'] = 1
            return response.json()
        except:
            self.status['get_data'] = 0

    def post_data(self, tab0_text2, tab0_text3, tab0_text4, tab0_text5):
        """上报数据"""
        try:
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
            # tab0_text2网内售电量
            # tab0_text3网外售电量
            # tab0_text4网内外售电量比
            # tab0_text5总售电量
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
            self.status['post_data'] = 1
        except:
            self.status['post_data'] = 0

    def feedback(self):
        """效验上报情况，反馈"""
        pass

    def send_email(self, from_addr, email_password, to_addr, smtp_server, fb):
        """对上报情况通过email通知用户"""
        # 运行结果
        # 发送相关信息，应html的格式展示
        msg = MIMEText('<html><body><h1>' + fb + '</h1>' +
            '<p>send by administrator</p>' + '</body></html>', 'html', 'utf-8')
        msg['From'] = utils.formataddr([u'售电日报自动上报客户端', from_addr])
        msg['To'] = utils.formataddr([u'管理员', to_addr])
        msg['Subject'] = Header(fb, 'utf-8').encode()
        try:
            # 服务器配置
            server = smtplib.SMTP(smtp_server, 25)
            # 打印出和SMTP服务器交互的所有信息
            # server.set_debuglevel(1)
            server.login(from_addr, email_password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
            self.status['send_email'] = 1
        except:
            self.status['send_email'] = 0

    def close_windows(self):
        """关闭所有窗口"""
        self.driver.quit()

    def run(self):
        """整体封装运行"""
        #
        ret = True
        # 打开界面，登录系统
        self.operation_auth(self.url, self.username, self.password)
        # 从售电API端口提取数据
        api_data_res = self.get_data(self.api_url)
        if self.status['operation_auth'] == 1:
            if self.status['get_data'] == 1:
                # 电量需除以10，占比需要四舍五入取整数
                # wangwai:网外售电量
                # wangwaiProp:网外电量占比
                # wangnei:网内售电量
                # wangneiProp:网内电量占比
                # total:总电量
                wangnei = str(float(api_data_res['value']['wangnei']) / 10.0)
                wangwai = str(float(api_data_res['value']['wangwai']) / 10.0)
                total = str(float(api_data_res['value']['total']) / 10.0)
                prop = u'{:0.0f}:{:0.0f}'.format(
                    float(api_data_res['value']['wangneiProp']),
                    float(api_data_res['value']['wangwaiProp']))
                # 上报数据
                self.post_data(wangnei, wangwai, prop, total)
                # 效验上报情况，反馈
                if self.status['post_data'] == 1:
                    fb = u'已正常上报晋能售电公司售电日报'
                else:
                    fb = u'发生错误，请核查'
                # 对上报情况通过email通知用户
                self.send_email(self.from_addr, self.email_password,
                                self.to_addr, self.smtp_server, fb)
                if self.status['send_email'] == 0:
                    print("发送email有故障，请核实")
                # 关闭所有窗口
                self.close_windows()
            else:
                self.close_windows()
                print('API取数异常')
                if self.status['get_data'] == 0:
                    fb = u'请予以核实API取数情况'
                # 对上报情况通过email通知用户
                    self.send_email(self.from_addr, self.email_password,
                                    self.to_addr, self.smtp_server, fb)
                if self.status['send_email'] == 0:
                    print("发送email有故障，请核实")
        else:
            print("浏览器打开异常")
            if self.status['operation_auth'] == 0:
                fb = u'请予以核实浏览器打开情况'
            # 对上报情况通过email通知用户
                self.send_email(self.from_addr, self.email_password,
                                self.to_addr, self.smtp_server, fb)
            if self.status['send_email'] == 0:
                print("发送email有故障，请核实")
            # 整体封装运行


if __name__ == '__main__':
    # 读取配置文件
    ret_con = read_config('web_post.config')
    if ret_con['status_code'] == 1:
        config = ret_con['value']
    else:
        print('文件读取失败！')
    web_post = WebPost(config['path'], config['api_url'], config['url'],
                       config['username'], config['password'],
                       config['from_addr'], config['email_password'],
                       config['to_addr'], config['smtp_server'])
    # web_post.operation_auth(config['url'], config['username'], config['password'])
    # web_post.send_email(config['from_addr'], config['email_password'], config['to_addr'], config['smtp_server'], u'此条信息用于测试使用')
    web_post.run()


