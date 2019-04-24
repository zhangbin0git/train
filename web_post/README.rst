===================
售电公司自动填报日报表
===================

目的
=====

向晋能电力集团生产管理信息系统自动填报日报表

工具版本
====================

:Python:     3.6.2
:pip:        
:virtualenv: 


安装与启动方法
=======================

从版本库获取代码，然后在该目录下搭建virtualenv环境::

   $ hg clone git@github.com:zhangbin0git/security.git
   $ cd security
   $ virtualenv .venv
   $ source .venv/bin/activate
   (.venv)$ pip install .
   (.venv)$ security
    * Running on http://127.0.0.1:5000/


开发流程
=========

用于开发的安装
------------------

1. 检测
2. 按以下流程安装::

     (.venv)$ pip install -e .

结构设计
------------------
# 前台开启浏览器模式
# 用户登录授权操作
# 从售电API端口提取数据
# 上报数据
# 效验上报情况，反馈
# 对上报情况通过email通知用户

变更依赖库时
---------------------

1. 更新``setup.py``的``install_requires``
2. 按以下流程更新环境::

     (.venv)$ virtualenv --clear .venv
     (.venv)$ pip install -e ./security

3. 将setup.py提交到版本库

变更依赖库时
---------------------

1. 更新``setup.py``的``install_requires``
2. 按以下流程更新环境::

     (.venv)$ virtualenv --clear .venv
     (.venv)$ pip install -e ./security
     (.venv)$ pip freeze > requirements.txt

3. 将setup.py和requirements.txt提交到版本库


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



