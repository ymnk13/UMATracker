#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last-Updated : <2015/06/12 13:40:51 by ymnk>
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from structDB import Base, Point
import numpy as np
import copy
import matplotlib.pyplot as plt
from matplotlib import lines

def main():
    engine = create_engine('sqlite:///rejectData0.db')#, echo=True)
    Base.metadata.create_all(engine) 
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()

    T = 30
    startT = 0
    endT = startT+T


    nextDB = session.query(Point).filter(Point.frameN == T).all()
    dt = 5
    N = len(nextDB)
    graph = []
    for t in xrange(endT,startT-1,-1):
        
        preDB = session.query(Point).filter(Point.frameN == t-1).all()
        nowDB = session.query(Point).filter(Point.frameN == t).all()
        matrix = np.zeros((len(preDB),len(nowDB)))
        for i in xrange(len(preDB)):
            for j in xrange(len(nowDB)):
                matrix[j][i] = preDB[i].dist(nowDB[j])
        graph.append(matrix)
    graph.reverse()
    graph = graph[1:]
    
    lineDatas = []
    for k in xrange(N):
        graphOLD = copy.deepcopy(graph)
        Z = 1000000
        
        for i in xrange(N):
            for j in xrange(N):
                graphOLD[0][i][j] = Z
        
        indeX = k
        graphOLD[0][indeX][indeX] = graph[0][indeX][indeX]
        lineDatas.append(getAll(graphOLD,N,indeX))
        
    
    fig, ax = plt.subplots(figsize = (10.0, 10.0))
    for i in [startT,endT]:
        dataC = session.query(Point).filter(Point.frameN == i).all()
        color = "red" if i == startT else "blue"
        for point in dataC:
            ax.scatter(point.y,point.x,color = color)

    """
    for i in xrange(29,0,-1):
        dataC = session.query(Point).filter(Point.frameN == i).all()
        for point in dataC:
            #plt.scatter(point.y,point.x,color = "yellow")
    """
    for e in xrange(N):
        for k in xrange(len(lineDatas)):
            print lineDatas[0][k]
            for i in xrange(29,1,-1):
                #print lineDatas[k][1][i-1],
                dataC = session.query(Point).filter(Point.frameN == i,Point.DogTag == lineDatas[k][e][i-1]).first()
                #ax.scatter(dataC.y,dataC.x,color = "purple")

                preDataC = session.query(Point).filter(Point.frameN == i-1,Point.DogTag == lineDatas[k][e][i-2]).first()
                ax.plot([preDataC.y,dataC.y],[preDataC.x,dataC.x])
    
    #ax.plot([0,700],[0,700])
    plt.show()


    """

    for t,k in enumerate(lineDatas[0]):
        for i in xrange(29,-1,-1):
            dataC = session.query(Point).filter(Point.frameN == i,Point.DogTag == k[i-1]).first()
            plt.scatter(dataC.y,dataC.x,color = "yellow")
        #break
    plt.show()
    """
def getAll(graph,N,indeX):
    Z = 1000000
    lists = []
    dic = dict([(j,[indeX,graph[0][j][j]]) for j in xrange(N)])
    lists.append(dic)

    for t in xrange(1,len(graph)-1):
        dic = dict([(j,[j,Z]) for j in xrange(N)])
        for i in xrange(N):
            cost = dic[i][1]
            for j in xrange(N):  
                cost = lists[-1][j][1]
                if not dic[i][1] >cost+graph[t][j][i]:
                    continue
                dic[i][1] = graph[t][j][i]+cost
                dic[i][0] = j
            dic[i][1] = dic[i][1]
        lists.append(dic)



    lines = []
    lines.append([i for i in xrange(N)])
    for t in xrange(len(lists)-1,0,-1):
        lines.append([lists[t][lines[-1][i]][0] for i in xrange(N)])
        
    lines = np.dstack(lines)[0]
    return lines


    """
    A = [( k,v) for k, v in lists[-1].iteritems()]
    lines = [min(A,key = lambda X : X[1][1])[1][0]]
    for t in xrange(len(lists)-2,0,-1):
        lines.append(lists[t][lines[-1]][0])
    """

        


if __name__  == "__main__":
    main()
