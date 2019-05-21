#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 19-5-20 下午12:38
# @Author  : Zhangbin
# @Site    : office
# @File    : ushuffle.py
# @Software: PyCharm

# from distutils.log import warn as printf
from os.path import dirname
from random import randrange as rand
from sqlalchemy import Column, Integer, String, create_engine, exc, orm
from sqlalchemy.ext.declarative import declarative_base

# 常量
COLSIZ = 10             # 左对齐，左侧空10个字符
DBNAME = 'test'
NAMELEN = 16
FIELDS = ('login', 'userid', 'projid')
RDBMSs = {'s': 'sqlite', 'm': 'mysql', 'g': 'gadfly'}
NAMES = (
    ('aaron', 8312), ('angela', 7603), ('dave', 7306),
    ('davina',7902), ('elliot', 7911), ('ernie', 7410),
    ('jess', 7912), ('jim', 7512), ('larry', 7311),
    ('leslie', 7808), ('melissa', 8602), ('pat', 7711),
    ('serena', 7003), ('stan', 7607), ('faye', 6812),
    ('amy', 7209), ('mona', 7404), ('jennifer', 7608),
)
DSNS = {
    'mysql': "mysql+mysqlconnector://zhangbin:zhangbin@localhost:3306/{}"
        .format(DBNAME),
    'sqlite': 'sqlite:///:memory:',
}

# 辅助函数
# 标题样式格式化函数，ljust左对齐
tformat = lambda s: str(s).title().ljust(COLSIZ)
cformat = lambda s: s.upper().ljust(COLSIZ)

# 用户选择数据库
def setup():
    return RDBMSs[input('''
Choose a database system:

(M)ySQL
(G)adfly
(S)QLite

Enter choice: ''').strip().lower()[0]]

# 随机名字，yield生成迭代器
def randName():
    pick = set(NAMES)
    while pick:
        yield pick.pop()

# 创建基类
Base = declarative_base()

class Users(Base):
    """继承基类，生成users表"""
    # 表名，必须有
    __tablename__ = 'users'
    login = Column(String(NAMELEN))
    userid = Column(Integer, primary_key=True)     #主键是必须的
    projid = Column(Integer)
    def __str__(self):
        return ''.join(map(tformat, (self.login, self.userid, self.projid)))

class SqlalchemyTest():
    # 操作数据库
    def __init__(self, dsn):
        try:
            eng = create_engine(dsn, echo=True)
        except ImportError:
            raise RuntimeError()

        try:
            eng.connect()
        except exc.OperationalError:
            # 连接到数据大库
            eng = create_engine(dirname(dsn))
            eng.execute('CREATE DATABASE %s' % DBNAME).close()
            eng = create_engine(dsn)

        # 当应用第一次载入时，我们定义一个Session类（声明Create_engine()的同时），
        # 这个Session类为新的Session对象提供工厂服务。
        Session = orm.sessionmaker(bind=eng)
        self.ses = Session()
        self.users = Users.__table__
        self.eng = self.users.metadata.bind = eng

    def insert(self):
        self.ses.add_all(
            Users(login=who, userid=userid, projid=rand(1,5)) \
            for who, userid in randName()
        )
        self.ses.commit()

    def update(self):
        fr = rand(1, 5)
        to = rand(1, 5)
        i = -1
        users = self.ses.query(
            Users).filter_by(projid=fr).all()
        for i, user in enumerate(users):
            user.projid = to
        self.ses.commit()
        return fr, to, i+1

    def delete(self):
        rm = rand(1,5)
        i = -1
        users = self.ses.query(
            Users).filter_by(projid=rm).all()
        for i, user in enumerate(users):
            self.ses.delete(user)
        self.ses.commit()
        return rm, i+1

    def dbDump(self):
        print('\n%s' % ''.join(map(cformat, FIELDS)))
        users = self.ses.query(Users).all()
        for user in users:
            print(user)
        self.ses.commit()

    def __getattr__(self, attr):    # use for drop/create
        return getattr(self.users, attr)

    def finish(self):
        self.ses.connection().close()

def main():
    print('*** Connect to %r database' % DBNAME)
    db = setup()
    if db not in DSNS:
        print('\nERROR: %r not supported, exit' % db)
        return
    try:
        orm = SqlalchemyTest(DSNS[db])
    except RuntimeError:
        print('\nERROR: %r not supported, exit' % db)
        return

    print('\n*** Create users table (drop old one if appl.)')
    orm.drop(checkfirst=True)
    orm.create()

    print('\n*** Insert names into table')
    orm.insert()
    orm.dbDump()

    print('\n*** Move users to a random group')
    fr, to, num = orm.update()
    print('\t(%d users moved) from (%d) to (%d)' % (num, fr, to))
    orm.dbDump()

    print('\n*** Randomly delete group')
    rm, num = orm.delete()
    print('\t(group #%d; %d users removed)' % (rm, num))
    orm.dbDump()

    print('\n*** Drop users table')
    orm.drop()
    print('\n*** Close cxns')
    orm.finish()

if __name__ == '__main__':
    main()

