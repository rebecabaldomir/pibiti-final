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

	def formatCNPJS(self, regras, cnpj):
			dados = []
			antes_da_seta = []
			depois_da_seta = []
			suporte = []
			confianca = []
			lift = []
			if(type(regras) == rpy2.rinterface.RNULLType):
				return dados
			cnpjs = self.extractCNPJs(regras)
			for label in regras[3]:
				suporte.append(label)

			for label in regras[4]:
				confianca.append(label)

			for label in regras[5]:
				lift.append(label)

			for i in range(0, len(cnpjs)):
				cnpjs[i].append(cnpj)
				vitorias = Banco().contaVitorias(cnpjs[i])
				print(vitorias)
				dados.append({
					'cnpj_1': cnpjs[i][0],
					'cnpj_2': cnpjs[i][1],
					'vitorias_1': vitorias[cnpjs[i][0]],
					'vitorias_2': vitorias[cnpjs[i][1]],
					'suporte': str(suporte[1]),
					'confianca': str(confianca[1]),
					'lift': str(lift[1])

				})

			return dados
	def extractCNPJs(self, regras):
		dados = []
		antes_da_seta = []
		depois_da_seta = []
		for label in regras[0].iter_labels():
				antes_da_seta.append(label)

		for label in regras[2].iter_labels():
			depois_da_seta.append(label)

		for i in range(0, len(antes_da_seta)):
				value1 = antes_da_seta[i].replace("{", "").replace("}","")
				value2 = depois_da_seta[i].replace("{", "").replace("}","")
				dados.append([value1, value2])
		return dados
				
	def contaVitorias(self, cnpjs):
		try:

		     conn = mysql.connector.connect(host="localhost",
					     user="root",
					     passwd="root",
					     db="mydb") 
		except:
		    print("I am unable to connect to the database")
	
		df = read_sql('select A.cnpj as cnpj1, A.valorpreco as preco1, B.cnpj as cnpj2, B.valorpreco as preco2, C.cnpj as cnpj3, C.valorpreco as preco3 ' +
			'from licitacoes as A  INNER JOIN licitacoes as B ON A.iditemcompra = B.iditemcompra ' +
			'INNER JOIN licitacoes as C ON B.iditemcompra = C.iditemcompra ' +
			'WHERE A.cnpj ='+cnpjs[0]+' and B.cnpj ='+cnpjs[1]+' and C.cnpj = '+cnpjs[2]+' ' +
			'and (A.valorpreco != \',0000\' or B.valorpreco != \',0000\' or C.valorpreco != \',0000\')', conn)
		conn.close()

		vitorias = {}
		vitorias[cnpjs[0]] = len(df[df['preco1'] != ',0000'])
		vitorias[cnpjs[1]] = len(df[df['preco2'] != ',0000'])
		vitorias[cnpjs[2]] = len(df[df['preco3'] != ',0000'])

		return vitorias