from Apriori import *
import os, os.path
import cherrypy
import rpy2.robjects as ro
import rpy2.robjects.packages as rpackages
from rpy2.robjects.packages import importr
import mysql.connector
from Banco import *


class AprioriApp(object):
	@cherrypy.expose
	def index(self):
		return open('view.html')
	
	def compras(self):
		return open('verifica_vencendor.html')

@cherrypy.expose
class AprioriCNPJ(object):
	@cherrypy.tools.json_out()
	def GET(self, cnpj):
		cnpjs = Banco().searchCNPJS(cnpj)
		regras = Apriori().extractRules(cnpjs)
		cnpjs = Banco().extractCNPJs(regras)
		
		return Banco().formatCNPJS(regras, cnpj)

@cherrypy.expose
class CompraPorCNPJ(object):
	@cherrypy.tools.json_out()
	def GET(self, idcompra):
		compras_cnpj = Banco().searchCompras(idcompra)
		return idcompra


if __name__ == '__main__':
	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.debug': True,
			'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
		},
		'/cnpj': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.response_headers.on': True,
			'tools.response_headers.headers': [('Content-Type', 'application/json')],
		},
		'/compras': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.response_headers.on': True,
			'tools.response_headers.headers': [('Content-Type', 'application/json')],
		},
		'/css': {
          'tools.staticdir.on': True,
          'tools.staticdir.dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css/')
        }
	}
	webapp = AprioriApp()
	webapp.cnpj = AprioriCNPJ()
	webapp.compras = CompraPorCNPJ()
	cherrypy.quickstart(webapp, '/', conf)
