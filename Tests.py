import unittest
from Apriori import *
from Banco import *

class Test(unittest.TestCase):

	def setUp(self):
		pass
 
	def test_zero_cnpjs_returned(self):
		self.AssertEqual(Banco().verifyWinner("00761025000108"), "NÃO")

if __name__ == '__main__':
    unittest.main()
