import mysql.connector
from pandas import *

class Banco(object):
	def searchCNPJS(self,cnpj):
		try:
		     conn = mysql.connector.connect(host="localhost",
					     user="root",
					     passwd="root",
					     db="mydb") 
		except:
		    print("I am unable to connect to the database")
		    
		dfsql = read_sql('select iditemcompra, cnpj from licitacoes where iditemcompra in (select iditemcompra from licitacoes where cnpj = ' + cnpj + ')  limit 50;', conn)
		conn.close()
		return dfsql

	def formatCNPJS(self, regras):
			dados = []
			antes_da_seta = []
			depois_da_seta = []
			print(regras[3])
			for label in regras[0].iter_labels():
				antes_da_seta.append(label)
			for label in regras[2].iter_labels():
				depois_da_seta.append(label)
			for i in range(0, len(antes_da_seta)):
				value1 = antes_da_seta[i].replace("{", "").replace("}","")
				value2 = depois_da_seta[i].replace("{", "").replace("}","")
				dados.append(value1 + " => " + value2)
				#dados.append(regras[3])
				#dados.append(regras[4])
			return dados

	def verififyWinner(self, cnpj):
		try:
		     conn = mysql.connector.connect(host="localhost",
					     user="root",
					     passwd="root",
					     db="mydb") 
		except:
		    print("I am unable to connect to the database")
		    
		result = read_sql('select valorpreco from licitacoes where cnpj= ' + cnpj + ')  limit 50;', conn)
		conn.close()
		if(result > 0):
			return "SIM"
		else:
			return "NAO"