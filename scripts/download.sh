mkdir downloads
cd downloads
mkdir hpo
cd hpo
wget http://purl.obolibrary.org/obo/hp/hpoa/genes_to_phenotype.txt 

cd ..
mkdir orphanet
cd orphanet
wget http://www.orphadata.org/data/xml/en_product6.xml

cd ..
mkdir omim
cd omim
wget https://omim.org/static/omim/data/mim2gene.txt
wget https://data.omim.org/downloads/2_y6sVJ5RaSk_jvrE_h9xw/mimTitles.txt
wget https://data.omim.org/downloads/2_y6sVJ5RaSk_jvrE_h9xw/genemap2.txt
wget https://data.omim.org/downloads/2_y6sVJ5RaSk_jvrE_h9xw/morbidmap.txt