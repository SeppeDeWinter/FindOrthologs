# Find ortholog genes 

## Usage

```python
FindOrthologs(features_file_path, homology_table_file_path, out_file_path)
```

Parameters:

```
features_file_path: path to 10x features.tsv.gz file

homology_table_file_path: path to orthologue table (see below)

out_file_path: path to file where result should be written
```

## orthology table

This is a table (tsv file) specifying gene orthologies, as can be downloaden from Biomart.

The table should have following format:


|  Species A gene Id   |   Species A gene Symbol  |  Species B gene Id  | Species B gene symbol |
|----|----|----|---|
| ...| ...| ...| ...|

With species A the species from which the features have to be converted (i.e its features are specified in features_file_path) and species B the species to which the gene names have to be converted to.

## Notes:
* This function only keeps one to one orthologues
* Genes which are not found in the orthology table will be indicated by: *NOT_IN_DB*
* Genes for which no orthology is known will be indicated by: *NO_ORTH*
* Genes which map to multiple genes (non one to one orthologues) will be indicated by: *MULTI_MAP*