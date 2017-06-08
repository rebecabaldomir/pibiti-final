import mysql.connector
import pandas as pd
from pandas import DataFrame
import csv

class APIBanco(object):

	def __init__(self):
		self.connect()

	
	def connect(self):
		self.db = mysql.connector.connect(host="localhost",    # your host, usually localhost
	                     user="root",         # your username
	                     passwd="root",  # your password
	                     db="mydb")        # name of the data base
		
	
	def search(self, cnpj):
		self.cur = self.db.cursor()

		query = ("select iditemcompra, cnpj from licitacoes where iditemcompra in (select iditemcompra from licitacoes where cnpj = '" + cnpj + "')  limit 50")

		self.cur.execute(query)

		return self.format()
	def buscarDadosCNPJs(self, cnpjs):
		self.cur = self.db.cursor()

		query = ("select iditemcompra, cnpj from licitacoes where iditemcompra in (select iditemcompra from licitacoes where cnpj = '" + cnpj + "')  limit 50")

		self.cur.execute(query)

		return self.format()

	def searchCNPJS(self, regras):
		#print(regras)
		dados = []
		antes_da_seta = []
		depois_da_seta = []
		for label in regras[0].iter_labels():
			antes_da_seta.append(label)
		
		for label in regras[2].iter_labels():
			depois_da_seta.append(label)
		#print(regras[0].iter_labels())
		print(str(regras[2]))
		#print(str(cnpjAlto))
		#print(str(cnpjs))
		for i in range(0, len(antes_da_seta)):
			value1 = antes_da_seta[i].replace("{", "").replace("}","")
			value2 = depois_da_seta[i].replace("{", "").replace("}","")
			dados.append(value1 + " => " + value2)
		print(dados)
		return dados
	
	def format(self):
		data = []
		for (iditemcompra, cnpj) in self.cur:
			data.append((iditemcompra, cnpj))
		#df = pd.DataFrame(data = data, columns=['id', 'cnpj'])
		with open('dadosParaAplicarRegras.csv', 'w') as f:
			writer = csv.writer(f)
			writer.writerows(data)
		self.close()
		return data

	def close(self):
		self.cur.close()
		self.db.close()

