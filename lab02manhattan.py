'''
Created on 18 giu 2017

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
from random import shuffle
from numpy import sqrt

NODES = 49
SQRT = int(sqrt(NODES))
PROBABILITY = 0.0


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


def routeTraffic(G, tsd):
    
    for n in G.edges():
        G.edge[n[0]][n[1]]['flow']=0
    # routing traffic                    
    for s in range(nx.number_of_nodes(G)):
        for d in range(nx.number_of_nodes(G)):
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


def simulatedAnnealing(G, tsd):
    
    thr_p=0.2
    
    flows=routeTraffic(G, tsd)
    fmax=max(flows)
    best_solution=G
    
    iterations=0
    
    while thr_p>0.001:
        iterations+=1
        node_a=0
        node_b=0
        while node_a==node_b:
            node_a=int(rnd.uniform(low=0,high=nx.number_of_nodes(G)))
            node_b=int(rnd.uniform(low=0,high=nx.number_of_nodes(G)))
            
        mapping={node_a:node_b,node_b:node_a}
        G_2=nx.relabel_nodes(G,mapping)
        
        flows=routeTraffic(G_2, tsd)
        if max(flows)<fmax:
            fmax=max(flows)
            print fmax
            best_solution=G_2
            G=G_2
        
        else:
            prob=rnd.uniform(low=0,high=1)
            if prob < thr_p:
                G=G_2
                thr_p=0.6*thr_p
                
        
    return best_solution, iterations


if __name__ == '__main__':
    tsd=generateTrafficMatrix(NODES, PROBABILITY)
    
    G=nx.grid_graph(dim=[SQRT,SQRT], periodic=True)
   
    tsd_2=copy.copy(tsd)
    
    # we create a list with the total amount of traffic exchanged between each pair of nodes
    traffic_list=[]
    for s in range(NODES):
        for d in range(NODES):
            if tsd_2[s][d]>0:
                traffic_list.append([[s,d],tsd_2[s][d]+tsd_2[d][s]])
                tsd_2[s][d]=0
                tsd_2[d][s]=0
    
    # we order the elements of the list in 
    traffic_list=sorted(traffic_list,key=lambda x: x[1], reverse=True)
    print traffic_list
 
    
    edj = nx.edges(G)
    shuffle(edj)
    
    assigned_nodes=[]
    for sd in traffic_list:
        if sd[0][0] not in G.nodes():
            if sd[0][1] not in G.nodes():
                e = edj.pop()
                mapping={e[0]:sd[0][0],e[1]:sd[0][1]}
                G=nx.relabel_nodes(G,mapping)
                assigned_nodes.append(sd[0][0])
                assigned_nodes.append(sd[0][1])
            else:
                for n in G.neighbors(sd[0][1]):
                    if n not in assigned_nodes:
                        mapping={n:sd[0][0]}
                        G=nx.relabel_nodes(G,mapping)
                        assigned_nodes.append(sd[0][0])
                        break
        elif sd[0][1] not in G.nodes():
            for n in G.neighbors(sd[0][0]):
                if n not in assigned_nodes:
                    mapping={n:sd[0][1]}
                    G=nx.relabel_nodes(G,mapping)
                    assigned_nodes.append(sd[0][1])
                    break
                        
    flows=routeTraffic(G, tsd)   
    fmax=max(flows)
    print fmax

    best,n_iterations=simulatedAnnealing(G, tsd)
    flows=routeTraffic(best, tsd)   
    fmax_best=max(flows)
    
    print "Best solution: " + str(fmax_best)
    print "N. iterations: " + str(n_iterations)

                        


    nx.draw(G,with_labels = True)
    plt.savefig("manhattan.png")