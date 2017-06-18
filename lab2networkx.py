'''
Created on 15 giu 2017

@author: jimmijamma
'''

import networkx as nx
import matplotlib.pyplot as plt
from numpy import random as rnd
from numpy import fill_diagonal
from numpy import argmax
from numpy import unravel_index
from numpy import zeros
import copy

NODES = 10
DELTA = 3
PROBABILITY = 0.1

def generateTrafficMatrix(n_nodes, probability):
    tsd=zeros((n_nodes,n_nodes))
    for s in range (n_nodes):
        for d in range (n_nodes): 
            prob=rnd.uniform(low=0,high=1)
            if prob > probability:
                tsd[s][d]=rnd.uniform(low=0.5,high=1.5)
            else:
                tsd[s][d]=rnd.uniform(low=5,high=15)
    fill_diagonal(tsd,0.0)
    return tsd


def routeTraffic(G, tsd, n_nodes):
    # routing traffic                    
    for s in range(n_nodes):
        for d in range(n_nodes):
            if tsd[s][d]>0:
                P=nx.shortest_path(G,s,d)
                for i in range(len(P)-1):
                    G.edge[P[i]][P[i+1]]['flow']+=tsd[s][d]
                
    flows=[]
    for e in G.edges():
        i=e[0]
        j=e[1]
        flows.append(G.edge[i][j]['flow'])
        
    return flows




if __name__ == '__main__':
    
    tsd=generateTrafficMatrix(NODES, PROBABILITY)
    
    G=nx.DiGraph()
    
    for i in range (NODES):
        G.add_node(i, n_lasers=DELTA, n_photodiods=DELTA)
        
    tsd_2=copy.copy(tsd)
    for i in range (NODES):
        j=(i+1)%NODES
        G.add_edge(i,j, flow=0)
        G.node[i]['n_lasers']-=1
        G.node[j]['n_photodiods']-=1
        tsd_2[i][j]=0
        
        
    maxima=[]
        
    while True:
        ind=argmax(tsd_2)
        amax=unravel_index(ind,(NODES,NODES))
        s_star=amax[0]
        d_star=amax[1]
        if tsd_2[s_star,d_star]>0:
            maxima.append([s_star,d_star])
            tsd_2[s_star,d_star]=0
        else:
            break
        

    for couple in maxima:
        s=couple[0]
        d=couple[1]
        if G.node[s]['n_lasers']>0:
            if G.node[d]['n_photodiods']>0:
                G.add_edge(s,d, flow=0)
                G.node[s]['n_lasers']-=1
                G.node[d]['n_photodiods']-=1
                tsd_2[s_star][d_star]=0


    flows=routeTraffic(G, tsd, NODES)
    fmax=max(flows)
    print fmax

    edge_labels = nx.get_edge_attributes(G,'flow')


    nx.draw_circular(G,with_labels = True, node_color='y')

    plt.savefig("path.png")