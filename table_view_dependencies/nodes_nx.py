# Visualize schema graph
import networkx as nx
import matplotlib.pyplot as plt
from nxviz.plots import CircosPlot, MatrixPlot, BasePlot, ArcPlot
import build_graph

G = build_graph.build_object_graph()

# Check basics: number of nodes, number of edges; for test data: 6, 16
num_nodes = len(G.nodes())
num_edges = len(G.edges())

# create subgroups of nodes and color as a preparation for drawing
tl_nodes = [n for n,v in G.nodes(data=True) if v['label'] == 'tableload'] 
vd_nodes = [n for n,v in G.nodes(data=True) if v['label'] == 'viewdef'] 
tl_edges = [(e,f) for e,f,v in G.edges(data=True) if v['label'] == 'tableload'] 
vd_edges = [(e,f) for e,f,v in G.edges(data=True) if v['label'] == 'viewdef']

# # nx draw: set positions
pos = nx.spring_layout(G)  # positions for all nodes
# # First, draw nodes from table load
nx.draw_networkx_nodes(G, pos, nodelist=tl_nodes, node_color='b')
nx.draw_networkx_nodes(G, pos, nodelist=vd_nodes, node_color='r')
nx.draw_networkx_edges(G, pos, edgelist=tl_edges, edge_color='b')
nx.draw_networkx_edges(G, pos, edgelist=vd_edges, edge_color='r')
nx.draw_networkx_labels(G,pos)
nx.draw_networkx_edge_labels(G,pos)

# nx.draw_networkx_labels(G)
plt.show() 

# some plots
#cpt = CircosPlot(graph=G, node_labels=True, node_color='label', edge_color='label')
#
cpt = CircosPlot(graph=G, node_labels=True)
cpt.draw()
plt.show()

nx.draw_kamada_kawai(G)
# nx.draw_networkx_labels(G)
# nx.draw_networkx_edge_labels(G)
plt.show()
#  plt.savefig("path.png")

# schema_dc = nx.degree_centrality(G)
# G_undir=G.to_undirected()
# some_nodes = ['B', 'STG_C', 'C']
# G_ppt_nodes = G_undir.subgraph(some_nodes)

in_degrees_dict = dict(G.in_degree())

plt.bar(range(len(in_degrees_dict)), list(in_degrees_dict.values()), align='center')
plt.xticks(range(len(in_degrees_dict)), list(in_degrees_dict.keys()), fontsize=5, rotation=30)
plt.title("in_degrees")
plt.show()

