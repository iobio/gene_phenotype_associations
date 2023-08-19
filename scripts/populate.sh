echo 'CREATING SCHEMA...'
sqlite3 gene_to_phenotype.db < sql/schema.sql

echo
echo 'POPULATING gene_to_phenotype TABLE...'
sqlite3 gene_to_phenotype.db < sql/populate_gene_to_phenotype.sql

echo
echo 'POPULATING gene_to_disorder TABLE...'
python src/populate_gene_to_disorder.py
