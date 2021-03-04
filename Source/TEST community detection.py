import networkx as nx
import operator
from matplotlib import pyplot as plt
import networkx.algorithms.community as nx_comm

# List of nodes
nodes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

#list of edges

edges = [(1, 2), (1, 4), (2, 4), (3, 7), (3, 5), (3, 6), (4, 5), (5, 7), (5, 6), (6, 7), (6, 21),
         (11, 21), (10, 21), (10, 11), (9, 10), (10, 13), (8, 9), (9, 12), (13, 14), (13, 18),
         (14, 20), (19, 20), (16, 20), (17, 20), (15, 16), (16, 17), (16, 18), (5, 13), (4, 19)]

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# for i in range(len(edges)):
#     betweenness = nx.edge_betweenness_centrality(G, k=None, normalized=True, weight=None, seed=None)
#     maxedge = max(betweenness.items(), key=operator.itemgetter(1))[0]
#     G.remove_edge(*maxedge)
#     # H = nx.connected_components(G)
#     # nx.draw(H, with_labels=True)
#     # plt.show()
#     comp = nx.algorithms.community.centrality.girvan_newman(G, most_valuable_edge=None)
#     list = tuple(sorted(c) for c in next(comp))
#     modularity = nx.algorithms.community.quality.modularity(G,list)
#     print(modularity)
#
#     nx.draw(G, with_labels=True)
#     plt.show()
#
# nx.draw(G, with_labels = True)
# plt.show()

# print("Nodes of graph: ")
# print(G.nodes())
# print("Edges of graph: ")
# print(G.edges())
