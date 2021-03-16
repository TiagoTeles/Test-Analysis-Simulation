import networkx as nx
import matplotlib.pyplot as plt
import random
import igraph as ig


g = ig.Graph()

# List of vertices
vertices = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

#list of edges
edges = [(0,1),(0,3),(1,3),(2,6),(2,4),(2,5),(3,4),(4,6),(4,5),(5,6),(5,20),(10,20),(9,20),(9,10),(8,9),(9,12),(7,8),(8,11),(12,13),(12,17),(13,19),(18,19),(15,19),(16,19),(14,15),(15,16),(15,17),(4,12),(3,18)]


g.add_vertices(21)
g.add_edges(edges)

def commmunities(graph, method):

    #EDGE_BETWEENNESS most exact but also slowest and most computor heavy
    #time = 946.8 s (edge) + 353.9 s (vertex)
    if method == 'edge_betweenness':
        v = g.community_edge_betweenness()
        clusters = v.as_clustering()
    
    #INFOMAP this one should specifically be for directed graphs but im not sure if we need to detect communities with the graph being directed
    if method == 'infomap':
        v = g.community_infomap()
        clusters = v

    #FAST_GREEDY & MULITLEVEL (very similar) fast but less accurate
    if method == 'fast_greedy':
        v = g.community_fastgreedy()
        clusters = v.as_clustering()
    elif method == 'multilevel':
        v = g.community_multilevel()
        clusters = v
    
    #WALKTRAP less fast than FAST_GREEDY but slightly more accurate
    if method == 'walktrap':
        v = g.community_walktrap()
        clusters = v.as_clustering()
    
    #LEIDEN algorithm should also be good but only for undirected graphs
    if method == 'leiden':
        v = g.community_leiden()
        clusters = v
    


    return clusters

methods = ["edge_betweenness", "infomap", "fast_greedy", "multilevel", "walktrap", "leiden" ]
clusters = commmunities(g, methods[5])

g.vs['label'] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13","14", "15", "16", "17","18", "19", "20", "21"]
layout = g.layout("kk")
ig.plot(clusters, layout = layout)
