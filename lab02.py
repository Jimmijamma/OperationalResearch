'''
Created on 14 giu 2017

@author: jimmijamma
'''

from numpy import random as rnd
from numpy import fill_diagonal
from numpy import argmax
from numpy import unravel_index



NODES=4
DELTA=2

class Graph():
    
    def __init__(self, n_nodes, delta):
        self.n_nodes=n_nodes
        self.delta=delta
        self.node_list = [Node(id, self.delta) for id in range(self.n_nodes)]
        self.tsd=self.generateTrafficMatrix(n_nodes)
        self.lp_list = []
        
    def generateTrafficMatrix(self,n_nodes):
        tsd=rnd.uniform(low=0.5,high=1.5,size=(n_nodes,n_nodes))
        fill_diagonal(tsd,0.0)
        print tsd
        return tsd
    
class TrafficMatrixCell():
    
    def __init__(self, source, destination):
        self.source=source
        self.destination=destination
        self.traffic=0
        if source!=destination:
            self.traffic=rnd.uniform(low=0.5,high=1.5)
        
    
class Node():
    
    def __init__(self, id, delta):
        self.id=id
        self.photodiods=delta
        self.lasers=delta
        
    
class Lightpath():
    
    def __init__(self,source, destination, graph):
        self.source=source
        self.destination=destination
        self.graph=graph
        self.id=[source,destination]
        self.graph.lp_list.append(self)
        
        for node in graph.node_list:
            if node==source:
                node.lasers=node.lasers-1
            if node==destination:
                node.photodiods=node.photodiods-1
        
        self.graph.tsd[source.id,destination.id]=0
   
        
def incrementalAlgorithm(graph):
    
    flag=False
    
    while flag==False:
    
        ind=argmax(graph.tsd)
        amax=unravel_index(ind,(NODES,NODES))
        s_star=amax[0]
        d_star=amax[1]
        
        if graph.tsd[s_star,d_star]>0:
            flag=True
            for s in graph.node_list:
                if s.id==s_star:
                    if s.lasers>0:
                        for d in graph.node_list:
                            if d.id==d_star:
                                if d.photodiods>0:
                                    l=Lightpath(s,d,G)
                                    flag=False

        else:
            flag=True
            
    for link in graph.lp_list:
        [s,d]=link.id
        print "S: " + str(s.id) + "  D: " + str(d.id)



if __name__ == '__main__':
    
    G=Graph(NODES, DELTA)
    incrementalAlgorithm(G)
    print G.tsd
    
    for node in G.node_list:
        print "ID: " + str(node.id) + " LASERS: " + str(node.lasers) + " PHOTODIODS: " + str(node.photodiods)
    
    