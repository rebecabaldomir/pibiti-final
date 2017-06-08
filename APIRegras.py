import rpy2.robjects as ro
import rpy2.robjects.packages as rpackages
from rpy2.robjects.packages import importr

class APIRegras(object):

	def __init__(self):
		utils = rpackages.importr('utils')
		utils.chooseCRANmirror(ind=1) 
		if not rpackages.isinstalled("arules"):
			utils.install_packages("arules")
		arules = importr("arules")

	def applyApriori(self):
		ro.r("compras <- read.transactions(file = 'dadosParaAplicarRegras.csv', format = 'single', sep = ',', cols = c(1,2))")
		ro.r("rules <- apriori(data = compras, parameter = list(support=0.3, confidence=0.95))")
		regras = ro.r("inspect(head(sort(rules, by='lift'),15))")
		return regras