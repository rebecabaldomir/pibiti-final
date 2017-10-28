import mysql.connector
from pandas import *
import rpy2

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
			suporte = []
			confianca = []
			if(type(regras) == rpy2.rinterface.RNULLType):
				return dados
			for label in regras[0].iter_labels():
				antes_da_seta.append(label)

			for label in regras[2].iter_labels():
				depois_da_seta.append(label)

			for label in regras[3]:
				suporte.append(label)

			for label in regras[4]:
				confianca.append(label)

			for i in range(0, len(antes_da_seta)):
				value1 = antes_da_seta[i].replace("{", "").replace("}","")
				value2 = depois_da_seta[i].replace("{", "").replace("}","")
				dados.append(value1 + " => " + value2 + " => " + str(suporte[1]) + " => " + str(confianca[1]))
			return dados

	#def searchCompras(self, idcompra)
	#	try:
	#		conn = mysql.connector.connect(host="localhost",
	#					     user="root",
	#					     passwd="root",
	#					     db="mydb") 
	#	except:
	#		print("I am unable to connect to the database")
	#		    
	#	dfsql = read_sql('select iditemcompra, cnpj from licitacoes where iditemcompra =' + idcompra + ')  limit 50;', conn)
	#	conn.close()
	#	return dfsql
