#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last-Updated : <2015/06/12 13:42:16 by ymnk>

import sqlite3
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm.session import sessionmaker
Base = declarative_base()

class Point(Base):
    __tablename__ = 'points'
    id = Column(Integer,primary_key = True)
    frameN = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    DogTag = Column(Integer) # Identification
    def __repr__(self):
        return "<Point(x='%f',y='%f'>"%(self.x,self.y)
    def dist(self,point):

        import numpy as np
        return np.linalg.norm(np.array([self.x,self.y])-
                              np.array([point.x,point.y]))


def main():
    engine = create_engine('sqlite:///acceptData2.db', echo=True)
    Base.metadata.create_all(engine) 
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()

    
    conn = sqlite3.connect('acceptData.db')
    cur = conn.cursor()
    cur.execute("""SELECT id,frameN,x,y,DogTag FROM dates ORDER by frameN;""")
    for name in cur.fetchall():
        id,frameN,x,y,DogTag = name
        p = Point(frameN = frameN,x = x,y = y, DogTag = DogTag)
        session.add(p)
    session.commit()
    

    fi = session.query(Point).all()
    print len(fi)

if __name__  == "__main__":
    main()
