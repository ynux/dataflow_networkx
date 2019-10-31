import build_graph 
import add_columns_graph
import networkx as nx
import nxviz
import matplotlib.pyplot as plt

G = build_graph.build_object_graph("test")
add_columns_graph.add_columns_graph(G, "test")

n_nodes = len(G.nodes())
n_edges = len(G.edges())

column_name = 'cola'

tabs_with_col = [n for n in G.neighbors(column_name)]
#G_undir=G.to_undirected()
#G_col_undir = G_undir.subgraph(tabs_with_col)
G_col = G.subgraph(tabs_with_col)


# create subgroups of nodes and color as a preparation for drawing
tl_edges = [(e,f) for e,f,v in G_col.edges(data=True) if v['label'] == 'tableload'] 
vd_edges = [(e,f) for e,f,v in G_col.edges(data=True) if v['label'] == 'viewdef']
#cl_edges = [(e,f) for e,f,v in G_col.edges(data=True) if v['label'] == 'column']
for n,d in G.nodes(data=True):
    try: 
        print(n, d['type'])
    except: 
        print(n,d)

views = [n for n,v in G_col.nodes(data=True) if v['type'] and v['type'] == 'VIEW']
tables = [n for n,v in G_col.nodes(data=True) if v['type'] and v['type'] == 'BASE TABLE']
# not part of the subgraph, only used for finding the tables and views:
# columns = [n for n,v in G_col.nodes(data=True) if v['type'] and v['type'] == 'COLUMN']

# # nx draw: set positions
#pos = nx.spring_layout(G_col)  # positions for all nodes
pos = nx.kamada_kawai_layout(G_col)  # positions for all nodes
# # First, draw nodes from table load
nx.draw_networkx_nodes(G_col, pos, nodelist=views, node_color='b')
nx.draw_networkx_nodes(G_col, pos, nodelist=tables, node_color='r')
#nx.draw_networkx_nodes(G_col, pos, nodelist=columns, node_color='m')
nx.draw_networkx_edges(G_col, pos, edgelist=tl_edges, edge_color='b')
nx.draw_networkx_edges(G_col, pos, edgelist=vd_edges, edge_color='r')
#nx.draw_networkx_edges(G_col, pos, edgelist=cl_edges, edge_color='m')

nx.draw_networkx_labels(G_col,pos)
#nx.draw_networkx_edge_labels(G_col,pos)

# nx.draw_networkx_labels(G)
plt.show() 

indegree_zero_nodes = [n for n in G_col.nodes() if G_col.in_degree(n) == 0]
print(indegree_zero_nodes)


if __name__ == "__main__":
    pass
