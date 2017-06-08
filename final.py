import os, os.path
import cherrypy
import rpy2.robjects as ro
import rpy2.robjects.packages as rpackages
from rpy2.robjects.packages import importr
import mysql.connector
from APIBanco import *
from APIRegras import *
import time


class AprioriApp(object):
	@cherrypy.expose
	def index(self):
		return open('interface.html')

@cherrypy.expose
class AprioriAPI(object):
	@cherrypy.tools.json_out()
	def GET(self, cnpj):
		ini = time.time()
		data = APIBanco().search(cnpj)
		regras = APIRegras().applyApriori()
		cnpjs = APIBanco().searchCNPJS(regras)
		fim = time.time()
		print("\n\n\n\n\n\n TEMPO: \n\n\n\n\n\n", fim-ini)
		retorno = str(cnpjs)
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