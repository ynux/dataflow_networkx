* relative paths when digesting input data
* blank lines at the end of the csv input files provoke a `list index out of range` error
* we do a bit of data cleansing of the viewdefinition input, which is inconsistent - we should do that before and assume clean csv, else error out (maybe basic checks like csvclean)
* it's irritating that the schema nodes come in a set while the objects nodes come as a dict (because of the attributes). We maybe should make the set a dict.


## convenience

* when you change the data, tell the input to run again

