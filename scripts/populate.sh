

echo 'CREATING SCHEMA...'
sqlite3 gene_to_phenotype.db < sql/schema.sql

echo
echo 'POPULATING gene_to_phenotype TABLE...'
cut -f1-4 downloads/hpo/genes_to_phenotype.txt | uniq > downloads/hpo/genes_to_phenotype.unique.txt
sqlite3 gene_to_phenotype.db < sql/populate_gene_to_phenotype.sql

echo
echo 'POPULATING gene_to_disorder TABLE...'
python src/populate_gene_to_disorder.py
