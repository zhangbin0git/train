#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 19-5-21 下午4:02
# @Author  : Zhangbin
# @Site    : 
# @File    : sqla_test.py
# @Software: PyCharm

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,MetaData
from sqlalchemy.orm import sessionmaker

# 常量
DATABASENAME = 'test'

# 创建引擎
engine = create_engine('mysql+mysqlconnector://zhangbin:zhangbin@'
                       'localhost:3306/{}'.format(DATABASENAME))

# 声明基类
Base = declarative_base()

# 创建类
class User(Base):
    __tablename__ = 'users'    #__tablename__是必须的
    id = Column(Integer, primary_key = True)  #主键是必须的
    name = Column(String(16))
    fullname = Column(String(16))
    password = Column(String(16))

class Work(Base):
    __tablename__ = 'works'    #__tablename__是必须的
    id = Column(Integer, primary_key = True)  #主键是必须的
    name = Column(String(16))
    fullname = Column(String(16))
    password = Column(String(16))

Base.metadata.create_all(engine)

# 当应用第一次载入时，我们定义一个Session类（声明Create_engine()的同时），
# 这个Session类为新的Session对象提供工厂服务。
Session = sessionmaker(bind=engine)
# 这个定制的Session类会创建绑定到数据库的Session对象。如果需要和数据库建立连接，
# 只需要实例化一个
session =Session()

# 添加对象
ed_user = User(name='ed', fullname='Ed join', password='desapssword')
ed_work = Work(name='two', fullname='myTwo', password='desapssword')
session.add(ed_user)
session.add(ed_work)
session.commit()

for instance in session.query(User).order_by(User.id).all():
    print(instance.name, instance.fullname)

print('-------------------------------------------------')

for name,fullname in session.query(User.name,User.fullname):
     print(name,fullname)

print('-------------------------------------------------')

for row in session.query(Work, Work.name).all():
    print(row.Work.id, row.name)
# print(input('stop:'))
session.connection().close()
# Work.metadata.drop_all(engine)


