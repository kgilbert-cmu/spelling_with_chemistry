import pandas

class PeriodicTable:
	def __init__(self, data = "data/periodic_table.tsv"):
		table = pandas.read_csv(data, sep = "\t")
		self.table = table
		self.sym_to_ele = dict(zip(table["Symbol"], table["Element"]))
		self.sym_to_w = dict(zip(table["Symbol"], table["Atomic Weight"]))
		self.ele_to_w = dict(zip(table["Element"], table["Atomic Weight"]))
	
	def getElement(self, symbol):
		return self.sym_to_ele[symbol]
	
	def allAbbrevs(self):
		return [s.lower() for s in self.table["Symbol"].values]
	
	def getWeight(self, symbol = None, element = None):
		if symbol is not None:
			val = self.sym_to_w[symbol]
		if element is not None:
			val = self.ele_to_w[element]
		try:
			val = float(val)
		except ValueError:
			val = float(val[1:-1]) # ignore parenthesis in '(123)'
		except NameError:
			# symbol and element not specified or not found
			return 0
		return val
