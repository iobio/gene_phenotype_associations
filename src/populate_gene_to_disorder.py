import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import sqlite3
from sqlite3 import Error

def main():
	print("connecting to db")
	conn = create_db_connection("gene_to_phenotype.db")

	print("reading Orphanet annotations xml file for disorder:gene associations")
	tree = ET.parse('downloads/orphanet/en_product6.xml')
	root = tree.getroot()

	for disorder in root.iter('Disorder'):
		disorder_name = disorder.find('Name').text
		orpha_code = disorder.find('OrphaCode').text
		for gene in disorder.iter('Gene'):
			gene_symbol = gene.find('Symbol').text
			row_id = insert_gene_to_disorder(conn, (gene_symbol, disorder_name, 'ORPHA:'+orpha_code, None))
			print(".", end ="", flush=True)



	print("\n", "reading OMIM txt file for disorder:gene associations")
	df = pd.read_csv('downloads/omim/genemap2.txt', sep="\t", header=3)
	for idx, row in df.iterrows():
		if ~np.isnan(row['MIM Number']):
			parent_mim_number   = row['MIM Number']
			gene_symbols = row['Gene Symbols']
			phenotypes  = row['Phenotypes']
			if type(row['Phenotypes']) == type('str'):
				if (len(phenotypes) > 0):
					phenotype_entries = phenotypes.split("; ")

					for phenotype_entry in phenotype_entries:

						tokens = phenotype_entry.split(", ")
						if (len(tokens) > 3):
							disorder =  tokens[0];

							for i in range(1, len(tokens) - 2):
								disorder += ", " + tokens[i]

							mim_number = tokens[len(tokens) - 2]
							inheritance = tokens[len(tokens) - 1]

						elif len(tokens) == 3:
							disorder    = tokens[0]
							mim_number  = tokens[1]
							inheritance = tokens[2]
						else:
							disorder = phenotype_entry
							mim_number = ""
							inheritance = None

					# strip the number in parenthesis off the end of the OMIM number
					idxParen = mim_number.find(" (")
					if idxParen > 0:
						mim_number = mim_number[0:idxParen]
					

					for gene_symbol in gene_symbols.split(", "):
						row_id = insert_gene_to_disorder(conn, (gene_symbol, disorder, 'OMIM:'+ mim_number, inheritance))
						print('.', end='', flush=True)

	print("\n", "done.")


def create_db_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def insert_gene_to_disorder(conn, gene_to_disorder):
    """
    Insert a row into gene_to_disorder table
    :param conn:
    :param gene_to_disorder dict:
    :return: row id
    """
    sql = ''' INSERT INTO gene_to_disorder(gene_symbol,disorder,disease_id,inheritance)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, gene_to_disorder)
    conn.commit()
    return cur.lastrowid    

if __name__ == '__main__':
    main()    

		

