# read from csv
# SCHEMA_NAME,OBJECT_NAME,REFERENCED_SCHEMA_NAME,REFERENCED_OBJECT_NAME,REFERENCED_OBJECT_TYPE
# STG_C,V_C1,B,T_B1,BASE TABLE
# STG_C,V_C2,B,T_B2,BASE TABLE
#
# ignore views and tables, only look at schemas
# 
# write files with nodes and edges to be digested by a networkx graph (multi digraph)
# parallel to write_node_dict_edge_list.py
# 

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--prefix", default="test",
                    help="prefix xxx of data/input/xxx_viewdefinitions.csv", metavar="FILE")

args = parser.parse_args()
inputfile = "./data/input/{0}_viewdefinitions.csv".format(args.prefix)
node_outputfile = "./data/intermediate/{}_viewdefinitions_schemaonly_nodes.pickle".format(args.prefix)
edge_outputfile = "./data/intermediate/{}_viewdefinitions_schemaonly_edges.pickle".format(args.prefix)

import csv, pickle

node_set = set()
edge_list = []

with open(inputfile) as f:
   csv_reader = csv.reader(f)
   line_count = 0
   for row in csv_reader:
     if line_count == 0:
       line_count += 1
     else:       # some functions diguised as views
       if not '(' in row[1]:
         # source views
         node_set.add(row[0].strip('\"'))
         # referenced tables / view
         node_set.add(row[2].strip('\"'))
         # edges
         edge_list.append( (row[2].strip('\"'), row[0].strip('\"') ))
         line_count += 1

with open(node_outputfile,'wb') as node_file:
    pickle.dump( node_set, node_file )

with open(edge_outputfile,'wb') as edge_file:
    pickle.dump( edge_list, edge_file )

