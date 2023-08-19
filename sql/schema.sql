DROP TABLE IF EXISTS gene_to_phenotype;
CREATE TABLE gene_to_phenotype (ncbi_gene_id text, 
	                            gene_symbol text NOT NULL,
	                            hpo_id text, 
	                            hpo_name text text NOT NULL, 
	                            frequency text,
	                            disease_id text);
CREATE INDEX gene_symbol_idx1 on gene_to_phenotype(gene_symbol);

DROP TABLE IF EXISTS gene_to_disorder;
CREATE TABLE gene_to_disorder (gene_symbol text NOT NULL, 
	                           disorder text NOT_NULL, 
	                           inheritance text, 
	                           disease_id text);
CREATE INDEX gene_symbol_idx2 on gene_to_disorder(gene_symbol);
