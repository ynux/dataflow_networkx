import networkx as nx
import build_graph

G = build_graph.build_object_graph()

# create subgroups of nodes and color as a preparation for drawing
tl_nodes = [n for n,v in G.nodes(data=True) if v['label'] == 'tableload'] 
vd_nodes = [n for n,v in G.nodes(data=True) if v['label'] == 'viewdef'] 
tl_edges = [(e,f) for e,f,v in G.edges(data=True) if v['label'] == 'tableload'] 
vd_edges = [(e,f) for e,f,v in G.edges(data=True) if v['label'] == 'viewdef']
views = [n for n,v in G.nodes(data=True) if v['type'] == 'VIEW']
tables = [n for n,v in G.nodes(data=True) if v['type'] == 'BASE TABLE']

# for test data
# find all nodes without incoming edges not in input layer
indegree_zero_not_input = []
for n,d in G.nodes(data=True):
    if d['schema'] != 'A' and G.in_degree(n) == 0:
        indegree_zero_not_input.append(n)

# find all nodes without outgoing edges not in output layer
outdegree_zero_not_output = []
for n,d in G.nodes(data=True):
    if d['schema'] != 'D' and G.out_degree(n) == 0:
        outdegree_zero_not_output.append(n)

# find all predecessors of an output node
table_predecs_set = set()
table_predecs_list = []
for p in G.predecessors('T_D1'):
    table_predecs_list.append(p)

added_nodes = len(table_predecs_list)
while added_nodes != 0:
     for n in table_predecs_list:
         added_nodes = 0
         for p in G.predecessors(n):
             table_predecs_list.append(p)
             added_nodes += 1

# find all successors of an input node

if __name__ == "__main__":
    print("number of nodes: {}".format(len(G.nodes())))
    print("number of edges: {}".format(len(G.edges())))
    print("nodes without incoming edges not in input layer: {}".format(indegree_zero_not_input))
    print("nodes without outgoing edges not in output layer: {}".format(outdegree_zero_not_output))
    print("predecessors of T_D1: {}".format(table_predecs_set))
    