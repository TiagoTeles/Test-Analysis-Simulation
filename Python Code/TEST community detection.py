import networkx as nx
from matplotlib import pyplot as plt

G=nx.Graph()

# List of nodes
nodes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

#list of edges
edges = [(1,2),(1,4),(2,4),(3,7),(3,5),(3,6),(4,5),(5,7),(5,6),(6,7),(6,21),(11,21),(10,21),
         (10,11),(9,10),(10,13),(8,9),(9,12),(13,14),(13,18),(14,20),(19,20),(16,20),(17,20),(15,16),(16,17),(16,18),(5,13),(4,19)]

G.add_nodes_from(nodes)
G.add_edges_from(edges)

# for i in range(1,21):
#     print("node",i, "has degree", G.degree(i))

betweenness = nx.edge_betweenness_centrality(G, k=None, normalized=True, weight=None, seed=None)


for i in range(len(edges)):
    print(betweenness[edges[i]])

print("Nodes of graph: ")
print(G.nodes())
print("Edges of graph: ")
print(G.edges())

nx.draw(G)
# plt.show()
