import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import sqlite3
from sqlite3 import Error
import sys
import re

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
			phenotypes_string  = row['Phenotypes']
			phenotypes = parse_phenotypes_string(phenotypes_string)
			for phenotype in phenotypes:
				for gene_symbol in gene_symbols.split(", "):
					row_id = insert_gene_to_disorder(conn, 
						(gene_symbol, phenotype['phenotype'], 
						'OMIM:'+ phenotype['mim_number'], 
						phenotype['inheritances']))
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

def parse_phenotypes_string(phenotypes_string):
	# Parse the phenotypes
	phenotypes = []

	if type(phenotypes_string) == type('str') and len(phenotypes_string) > 0:
		for phenotype in phenotypes_string.split(';'):
			# Clean the phenotype
			phenotype = phenotype.strip()

			# Long phenotype
			matcher = re.match(r'^(.*),\s(\d{6})\s\((\d)\)(|, (.*))$', phenotype)
			if matcher:

			# Get the fields
				phenotype = matcher.group(1)
				phenotypeMimNumber = matcher.group(2)
				phenotypeMappingKey = matcher.group(3)
				inheritances = matcher.group(5)

				# Get the inheritances, may or may not be there
				if inheritances:
					for inheritance in inheritances.split(','):
						inheritance = inheritance.strip()

				phenotypes.append(
					{'phenotype':   phenotype, 
					'mim_number':   phenotypeMimNumber, 
					'inheritances': inheritances })

			# Short phenotype
			else:

				# Short phenotype
				matcher = re.match(r'^(.*)\((\d)\)(|, (.*))$', phenotype)
				if matcher:

				  # Get the fields
					phenotype = matcher.group(1)
					phenotypeMappingKey = matcher.group(2)
					inheritances = matcher.group(3)

					# Get the inheritances, may or may not be there
					if inheritances:
						for inheritance in inheritances.split(','):
							inheritance = inheritance.strip()

					phenotypes.append(
						{'phenotype':   phenotype, 
						'mim_number':   '', 
						'inheritances': inheritances })

	return phenotypes

if __name__ == '__main__':
    main()    

		

