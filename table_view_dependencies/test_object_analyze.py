import networkx as nx
import build_graph

def find_nodes_indegree_zero_not_input_layer(G, input_layer, write_file=True):
    # find all nodes without incoming edges but not in input layer
    indegree_zero_not_input = []
    for n,d in G.nodes(data=True):
        if d['schema'] not in in_layer and G.in_degree(n) == 0:
            indegree_zero_not_input.append(n)
    
    if write_file:
        with open("./data/output/test_indegree_zero_not_input.csv", "w", newline="") as f:
            f.writelines("%s\n" % node for node in indegree_zero_not_input)

    return indegree_zero_not_input


def find_nodes_outdegree_zero_not_output_layer(G, output_layer, write_file=True):    
    # find all nodes without outgoing edges not in output layer
    outdegree_zero_not_output = []
    for n,d in G.nodes(data=True):
        if d['schema'] not in out_layer and G.out_degree(n) == 0:
            outdegree_zero_not_output.append(n)

    if write_file:
        with open("./data/output/test_outdegree_zero_not_output.csv", "w", newline="") as f:
            f.writelines("%s\n" % node for node in outdegree_zero_not_output)

    return outdegree_zero_not_output


def find_predecessors(G, start_node, with_schema=False, write_file=True):
    # find all predecessors of an output node
    table_predecs_list = []

    for p in G.predecessors(start_node):
        table_predecs_list.append(p)

    num_before = 0
    num_after = len(table_predecs_list)
    nodes_done = set()
    while (num_after > num_before):
        for n in table_predecs_list:
            if n not in nodes_done:
                num_before = len(table_predecs_list)
                for p in G.predecessors(n):
                    table_predecs_list.append(p)
                    nodes_done.add(n)
                    num_after = len(table_predecs_list)
    if with_schema:
        table_predecs_dict = {}
        for n in table_predecs_list:
            table_predecs_dict[n] = G.nodes[n]['schema']
    if with_schema and write_file:
        with open("./data/output/test_predecessors_of_{}_with_schema.csv".format(start_node), "w", newline="") as f:
            for node in table_predecs_dict:
                f.writelines("{},{}\n".format(node, table_predecs_dict[node]))
    
    if write_file:
        # the list preservers the order in which the nodes were found, but can contain duplicates
        with open("./data/output/test_predecessors_of_{}.csv".format(start_node), "w", newline="") as f:
            f.writelines("%s\n" % node for node in table_predecs_list)
        table_predecs_set = set(table_predecs_list)
        with open("./data/output/test_uniq_predecessors_of_{}.csv".format(start_node), "w", newline="") as f:
            f.writelines("%s\n" % node for node in table_predecs_set)
    return table_predecs_list

# find all successors of an input node

if __name__ == "__main__":
    G = build_graph.build_object_graph('test')
    out_layer = ['D']
    in_layer = ['A']
    start_node_output = 'T_D2'
    print("number of nodes: {}".format(len(G.nodes())))
    print("number of edges: {}".format(len(G.edges())))
    print("number of nodes without incoming edges not in input layer: {}".format(len(find_nodes_indegree_zero_not_input_layer(G, in_layer))))
    print("number of nodes without outgoing edges not in output layer: {}".format(len(find_nodes_outdegree_zero_not_output_layer(G, out_layer))))
    print("number of predecessors of {}: {}".format(start_node_output, len(find_predecessors(G,start_node_output, with_schema=True))))
    