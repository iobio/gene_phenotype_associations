# gene_phenotype_associations

Python scripts to load gene-to-phenotype db to supply gene to HPO terms (phenotypes) and gene to disease assocations.


## Generating the database

Get the code:
```
git clone https://github.com/iobio/gene_phenotype_associations
cd gene_phenotype_associations
```

Create a python environment and install pandas:
```
python3 -m venv g2p
source activate g2p/bin/activate.sh
pip install pandas
```

Generate the db:
```
./scripts/download.sh
./scripts/populate.sh
```


## Sources of data
gene to phenotypes    HPO       https://hpo.jax.org/app/data/annotations
gene to disease       Orphanet  http://www.orphadata.org/cgi-bin/index.php



