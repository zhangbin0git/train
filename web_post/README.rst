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
# 关闭所有窗口
# 整体封装运行

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




    # 方法主入口
    if __name__ == '__main__':
        # 加启动配置
        driver = openChrome(path)
        operationAuth(driver, url)
        # open_page(driver)



