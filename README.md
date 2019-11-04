# How this Works

### Assumption on the Underlying Data Flow

This code was written to create a graph from a data flow like the following one:

1. Tables are loaded, either from other tables, or from Views
2. Views are built from tables

We can extract information from the load toal and the view defining sql:

1.  For every loaded table: schema_name, table_name, source_schema_name, source_object_name, source_object_type. 
2. For every created view: schema_name, view_name, referenced_schema_name, referenced_object_name, referenced_object_type

### Input Format, and Rewriting it for Graph Digestion

This information comes as csv, like `test_tableload.csv` and `test_viewdefinitions.csv`. In our test data flow, a table is always created from only one view (or table). A view may use several tables, and a table may be referenced by several views.

Put your real data into `<prefix>_tableload.csv` and `<prefix>_viewdefinitions.csv`.

From one csv file, two pickle files are created: One containing the nodes (views and tables, with schema and type as attributes), the other the edges (references / loaded from). 
`viewdefinitions_graph_input.py` takes `prefix` as input and creates `<prefix>_viewdefinitions_nodes.pickle` and `<prefix>_viewdefinitions_edges.pickle`, 
`tableload_graph_input.py` takes `prefix` as input and creates `<prefix>_tableload_nodes.pickle` and `<prefix>_tableload_edges.pickle`. 

If you are only interested in the schemas:
`viewdefinitions_schemaonly_graph_input.py` creates `<prefix>_viewdefinitions_schemaonly_nodes.pickle` and `<prefix>_viewdefinitions_schemaonly_edges.pickle`, 
`tableload_schemaonly_graph_input.py` creates `<prefix>_tableload_schemaonly_nodes.pickle` and `<prefix>_tableload_schemaonly_edges.pickle`. 

### Playing With Graphs

_from here on, only notes_

Load the pickled node and edge information into a graph. DiGraph, MultiDiGraph

Create images, lists of predecessors, list of successors
Analysis of centrality

Bipartite graphs?

### Remark on Test Data

The test data is a simplified model of a datawarehouse with six layers:

* An input layer of tables **A**
* a second layer of tables **B** (e.g. to create history tables)
* a third layer of views **STG_C** (e.g. for some data cleaning)
* a fourth layer of tables **D** (think of these as materialized views of STG_C)
* a fifth layer of views **STG_D** (here, some serious joining is happening)
* a sixth layer of tables **D** (like materialized views of STG_D); this could be the final layer for consumption

While the first four layers are separate tracks and the relations are 1:1, from C to STG_D some join logic is applied and we have n:m dependencies. 
The table `T_B4` is a dead end and never consumed.
The table `T_C4` is a table coming in from some other system.
	
## Some Thoughts on Graphs

I enjoyed working with networkx, but will probably go back to using relational databases. 
I liked it because:

* It was good to think of data as a graph
* the notions of flow and predecessor / successor are good to model as a graph 
* questions like "are there any dead ends / views with no output 

I'll probably drop it because:

* The break between technologies (database - csv - graph) is expensive
* everything you can do in graph is also doable in tables
* visualization did not work as hoped for. networkx says [it's meant more for analysis than visualization](https://networkx.github.io/documentation/stable/reference/drawing.html). But analysis such as the distribution of centrality is not what people waited for. I tried to steer them away from wanting to see beautiful graphs, but it didn't work. I tried nxviz, which is convenient, but again not what people dreamed of. I'm not fluent in mathplotlib.pyplot. If you are, you'll be more successful. However, to get the results i need, at some point i'd have to go into positioning (attracting forces, and such).

 
