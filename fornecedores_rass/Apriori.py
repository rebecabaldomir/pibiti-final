from numpy import *
import scipy as sp
from pandas import *
import rpy2
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects
from rpy2.robjects import r, pandas2ri
import rpy2.robjects.packages as rpackages
from rpy2.robjects.packages import importr
import psycopg2
pandas2ri.activate()

class Apriori(object):
	
	def extractRules(self, cnpjs):
		robjects.globalenv['itens'] = cnpjs
		cnpjs.head()

		# import R's "packages
		base = importr('base')
		utils = importr('utils')
		arules = importr('arules')

		# using R
		r_split = robjects.r['split']
		r_list = robjects.r['list']
		r_as = robjects.r['as']
		r_apriori = robjects.r['apriori']
		r_inspect = robjects.r['inspect']
		splitdf = r_split(cnpjs.cnpj, cnpjs.iditemcompra)

		# apply apriori
		trans = r_as(splitdf, "transactions")
		rules = r_apriori(trans, parameter = r_list(minlen = 2,supp = 0.2, conf = 0.98, target = "rules"))
		teste = r_inspect(robjects.r["head"](robjects.r["sort"](rules, by="lift")
		#teste = r_inspect(robjects.r["sort"](teste, by="lift"));
		print(teste)
		return teste


