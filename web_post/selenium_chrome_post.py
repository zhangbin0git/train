#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019-4-3 18:23 
# @Author : Mark 
# @Site :  
# @File : selenium_chrome_post.py 
# @Software: PyCharm Community Edition

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import time
url = r"http://10.1.3.33:7001/Liems/"
path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

# 前台开启浏览器模式
def openChrome(path):
    # 打开chrome浏览器
    driver = webdriver.Chrome(path)
    return driver

# 授权操作
def operationAuth(driver, url):
    driver.get(url)
    # 找到输入框并输入查询内容
    luku_user = driver.find_element_by_id("userName")
    luku_user.send_keys("JNDLLLSD")
    luku_pwd = driver.find_element_by_id("password")
    luku_pwd.send_keys("1234")
    # 提交表单
    # "menuIdrandom5 splitLine topButton"
    driver.find_element_by_class_name("login_btn").click()
    # 以上完成登录工作

    # 点击数据上报按钮
    driver.find_element_by_xpath("//div[contains(text(), '数据上报')]").click()
    time.sleep(2)
    # driver.find_element_by_xpath(
    #     "//label[contains(text(), '晋能售电公司售电日报')]").click()
    # 点击晋能售电公司售电日报按钮
    mid = driver.find_element_by_xpath("//label[contains(text(), '售电日报')]")
    # time.sleep(3)
    mid.click()
    time.sleep(3)
    # 切换frame
    driver.switch_to_frame("mainFrame")
    # 点击新建按钮
    mik = driver.find_element_by_id("New")
    # time.sleep(3)
    mik.click()
    time.sleep(1)
    # 填入数据
    driver.find_element_by_id("tab0_text2").send_keys("1234")
    driver.find_element_by_id("tab0_text3").send_keys("1234")
    driver.find_element_by_id("tab0_text4").send_keys("1234")
    driver.find_element_by_id("tab0_text5").send_keys("1234")
    # 点击保存按钮
    driver.find_element_by_id("Save").click()
    time.sleep(1)
    # 点击所有操作按钮
    driver.find_element_by_id("taskDetail").click()
    # 点击提交按钮
    driver.find_element_by_class_name('wf_mouseout').click()
    driver.close()

    print('查询操作完毕！')


# def open_page(driver):
    # driver.driver.find_element_by_id("tree_NodeLabel_P6180").click()


# def sub_post(driver, url):
#     driver.get(url)

# 方法主入口
if __name__ == '__main__':
    # 加启动配置
    driver = openChrome(path)
    operationAuth(driver, url)
    # open_page(driver)
