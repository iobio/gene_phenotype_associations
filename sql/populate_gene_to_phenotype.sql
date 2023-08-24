delete from gene_to_phenotype;
.separator "\t"
.import downloads/hpo/genes_to_phenotype.unique.txt gene_to_phenotype
select count(*) from gene_to_phenotype;
