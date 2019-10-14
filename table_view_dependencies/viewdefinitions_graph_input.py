# read from csv
# SCHEMA_NAME,OBJECT_NAME,REFERENCED_SCHEMA_NAME,REFERENCED_OBJECT_NAME,REFERENCED_OBJECT_TYPE
# STG_C,V_C1,B,T_B1,BASE TABLE
# STG_C,V_C2,B,T_B2,BASE TABLE
#
# write files with node_dict, edges to be digested by a networkx graph
# remark: if you want to avoid using pickle, use json_dumps / json_loads for the dict. edge_list
# is a list of tuples, which makes things complicated and me use pickle.
# 
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--prefix", default="test",
                    help="prefix xxx of data/input/xxx_viewdefinitions.csv", metavar="FILE")

args = parser.parse_args()
inputfile = "./data/input/{0}_viewdefinitions.csv".format(args.prefix)
node_outputfile = "./data/intermediate/{}_viewdefinitions_nodes.pickle".format(args.prefix)
edge_outputfile = "./data/intermediate/{}_viewdefinitions_edges.pickle".format(args.prefix)

import csv, pickle

node_dict = {}
edge_list = []

with open(inputfile) as f:
   csv_reader = csv.reader(f)
   line_count = 0
   for row in csv_reader:
     if line_count == 0:
       line_count += 1
     else:
       # some functions diguised as views
       if not '(' in row[1]:
         node_dict[row[1].strip('\"')] = { 'schema': row[0].strip('\"'), 'type': 'VIEW'} 
         # referenced tables / view
         node_dict[row[3].strip('\"')] = { 'schema': row[2].strip('\"'), 'type': row[4].strip('\"')} 
         # edges
         edge_list.append( (row[3].strip('\"'), row[1].strip('\"') ))
         line_count += 1

with open(node_outputfile,'wb') as node_dict_file:
    pickle.dump( node_dict, node_dict_file )

with open(edge_outputfile,'wb') as edge_list_file:
    pickle.dump( edge_list, edge_list_file)

