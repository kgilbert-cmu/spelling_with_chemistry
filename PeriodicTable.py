import pandas

class PeriodicTable:
	def __init__(self, data = "data/periodic_table.tsv"):
		table = pandas.read_csv(data, sep = "\t")
		self.table = table
		self.sym_to_ele = dict(zip(table["Symbol"], table["Element"]))
	
	def getElement(self, symbol):
		return self.sym_to_ele[symbol]
	
	def allAbbrevs(self):
		return [s.lower() for s in self.table["Symbol"].values]
	
	
