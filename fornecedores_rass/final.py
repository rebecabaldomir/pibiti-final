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

@cherrypy.expose
class AprioriAPI(object):
	@cherrypy.tools.json_out()
	def GET(self, cnpj):
		cnpjs = Banco().searchCNPJS(cnpj);
		regras = Apriori().extractRules(cnpjs)
		cnpjs = Banco().formatCNPJS(regras)
		return cnpjs

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
		'/css': {
          'tools.staticdir.on': True,
          'tools.staticdir.dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css/')
        }
	}
	webapp = AprioriApp()
	webapp.cnpj = AprioriAPI()
	cherrypy.quickstart(webapp, '/', conf)
