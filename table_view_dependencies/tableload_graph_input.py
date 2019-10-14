# read from csv generated from table load tool
# DEST_SCHEMA_NAME,DEST_TABLE_NAME,SRC_SCHEMA_NAME,SRC_TABLE_NAME,REFERENCED_OBJECT_TYPE
# B,T_B1,A,T_A1,BASE TABLE
# B,T_B2,A,T_A2,BASE TABLE
#
# write files with node_dict, edges_list to be digested by a networkx graph, with schema and type as node attributes
# remark: if you want to avoid using pickle, use json_dumps / json_loads for the dict. edge_list
# is a list of tuples, which makes things complicated and me use pickle.
#  
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--prefix", default="test",
                    help="prefix xxx of data/input/xxx_tableload.csv", metavar="FILE")

args = parser.parse_args()
inputfile = "./data/input/{0}_tableload.csv".format(args.prefix)
node_outputfile = "./data/intermediate/{}_tableload_nodes.pickle".format(args.prefix)
edge_outputfile = "./data/intermediate/{}_tableload_edges.pickle".format(args.prefix)

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
         node_dict[row[1]] = { 'schema': row[0], 'type': 'BASE TABLE'} 
         # referenced tables / view
         node_dict[row[3]] = { 'schema': row[2], 'type': row[4]} 
         # edges
         edge_list.append( (row[3], row[1] ))
         line_count += 1

with open(node_outputfile,'wb') as node_dict_file:
    pickle.dump( node_dict, node_dict_file )

with open(edge_outputfile,'wb') as edge_list_file:
    pickle.dump( edge_list, edge_list_file)

