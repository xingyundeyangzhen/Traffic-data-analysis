import time
import sqlite3
import csv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,  create_engine, Float
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
DBSession = scoped_session(sessionmaker())
engine = None


class data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True)
    linkref = Column(String(20))
    linkdes = Column(String(255))
    date = Column(String(20))
    timeperiod = Column(Integer)
    avgJT = Column(Float)
    avgSpeed = Column(Float)
    dataQuality = Column(Integer)
    linklength = Column(Float)
    Flow = Column(Float)


def init_sqlalchemy(dbname='sqlite:///data.db'):
    global engine
    engine = create_engine(dbname, echo=False)
    DBSession.remove()
    DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_sqlalchemy_orm(n=100000):
    init_sqlalchemy()
    t0 = time.time()
    with open('MAR15.csv') as f:
        f_csv = list(csv.reader(f,delimiter=','))
        # headers = next(f_csv)
        for i in range(n):
            d = data()
            d.id = i+1
            d.linkref = f_csv[i+1][0]
            d.linkdes = f_csv[i+1][1]
            d.date = f_csv[i+1][2]
            d.timeperiod = f_csv[i+1][3]
            d.avgJT = f_csv[i+1][4]
            d.avgSpeed = f_csv[i+1][5]
            d.dataQuality = f_csv[i+1][6]
            d.linklength = f_csv[i+1][7]
            d.Flow = f_csv[i+1][8]
            DBSession.add(d)
            if not (i+1) % 10000:
                DBSession.flush()
    DBSession.commit()
    print(
        "SQLAlchemy ORM: Total time for " + str(n) +
        " records " + str(time.time() - t0) + " secs")




def test_sqlalchemy_orm_bulk_save_objects(n=100000):
    '''
    执行给定对象列表的批量保存。批量保存功能允许将映射对象用作简单的INSERT和UPDATE操作的源，这些操作可以更容易地分组到更高性能的“执行”操作中;也可以使用较低延迟的进程来执行数据从对象的提取，忽略在UPDATE的情况下属性是否已被实际修改，并且也忽略SQL表达式。
    '''
    init_sqlalchemy()
    t0 = time.time()
    with open('MAR15.csv') as f:
        f_csv = list(csv.reader(f,delimiter=','))
        datalist = []
        for i in range(n):
            d = data()
            d.id = i+1
            d.linkref = f_csv[i+1][0]
            d.linkdes = f_csv[i+1][1]
            d.date = f_csv[i+1][2]
            d.timeperiod = f_csv[i+1][3]
            d.avgJT = f_csv[i+1][4]
            d.avgSpeed = f_csv[i+1][5]
            d.dataQuality = f_csv[i+1][6]
            
            d.linklength = f_csv[i+1][7]
            d.Flow = f_csv[i+1][8]
            datalist.append(d)
            if not (i+1) % 10000:
                DBSession.bulk_save_objects(datalist)
                datalist = []
        DBSession.commit()
    print(
        "SQLAlchemy ORM bulk_save_objects(): Total time for " + str(n) +
        " records " + str(time.time() - t0) + " secs")
    
    
def test_sqlalchemy_orm_bulk_insert(n=100000):
    '''
    执行给定的映射字典列表的批量插入。批量插入功能允许使用简单的Python字典作为简单INSERT操作的源，可以更容易地将其组合到更高性能的“执行”操作中。使用字典，没有使用“历史”或会话状态管理功能，减少插入大量简单行时的延迟。
    '''
    init_sqlalchemy()
    t0 = time.time()
    with open('MAR15.csv') as f:
        f_csv = list(csv.reader(f,delimiter=','))
        datalist = []
        for i in range(n):
            dict(name="NAME " + str(i))
            d = dict()
            d['id'] = i+1
            d['linkref'] = f_csv[i+1][0]
            d['linkdes'] = f_csv[i+1][1]
            d['date'] = f_csv[i+1][2]
            d['timeperiod'] = f_csv[i+1][3]
            d['avgJT'] = f_csv[i+1][4]
            d['avgSpeed'] = f_csv[i+1][5]
            d['dataQuality'] = f_csv[i+1][6]
            d['linklength'] = f_csv[i+1][7]
            d['Flow'] = f_csv[i+1][8]
            datalist.append(d)
            if not (i+1) % 10000:
                DBSession.bulk_insert_mappings(data,datalist)
                datalist = []
        DBSession.commit()
    print(
        "SQLAlchemy ORM bulk_insert_mappings(): Total time for " + str(n) +
        " records " + str(time.time() - t0) + " secs")


def test_sqlalchemy_core(n=100000):
    init_sqlalchemy()
    t0 = time.time()
    datalist = []
    with open('MAR15.csv') as f:
        f_csv = list(csv.reader(f,delimiter=','))
        for i in range(n):
            dict(name="NAME " + str(i))
            d = dict()
            d['id'] = i+1
            d['linkref'] = f_csv[i+1][0]
            d['linkdes'] = f_csv[i+1][1]
            d['date'] = f_csv[i+1][2]
            d['timeperiod'] = f_csv[i+1][3]
            d['avgJT'] = f_csv[i+1][4]
            d['avgSpeed'] = f_csv[i+1][5]
            d['dataQuality'] = f_csv[i+1][6]
            d['linklength'] = f_csv[i+1][7]
            d['Flow'] = f_csv[i+1][8]
            datalist.append(d)
    engine.execute(data.__table__.insert(),datalist)  # ==> engine.execute('insert into table (column) values ("v1"), ("v2")')
    print(
        "SQLAlchemy Core: Total time for " + str(n) +
        " records " + str(time.time() - t0) + " secs")


def init_sqlite3(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS data")
    c.execute(
        "CREATE TABLE data (id INTEGER NOT NULL, "
        "linkref VARCHAR(20), \
         linkdes VARCHAR(255), \
         date VARCHAR(20), \
         timeperiod INTEGER,\
         avgJT FLOAT, \
         avgSpeed FLOAT,\
         dataQuality INTEGER,\
         linklength FLOAT,\
         Flow FLOAT,\
         PRIMARY KEY(id))")
    conn.commit()
    return conn


def test_sqlite3(n=100000, dbname='sqlite3.db'):
    conn = init_sqlite3(dbname)
    c = conn.cursor()
    t0 = time.time()
    with open('MAR15.csv') as f:
        f_csv = list(csv.reader(f,delimiter=','))
        for i in range(n):
            row = (i+1,f_csv[i+1][0],f_csv[i+1][1],f_csv[i+1][2],f_csv[i+1][3],
            f_csv[i+1][4],f_csv[i+1][5],f_csv[i+1][6],f_csv[i+1][7],f_csv[i+1][8],)
            c.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?,?)", row)
        conn.commit()
    print(
        "sqlite3: Total time for " + str(n) +
        " records " + str(time.time() - t0) + " sec")


if __name__ == '__main__':
    test_sqlalchemy_orm(100000)
    test_sqlalchemy_orm_bulk_save_objects(100000)
    test_sqlalchemy_orm_bulk_insert(100000)
    test_sqlalchemy_core(100000)
    test_sqlite3(100000)
