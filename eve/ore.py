from objects import Item
import util

class Ore(Item):
	def __init__(self, name, itemID, size, lower=0.0, upper=1.0):
		super(Ore, self).__init__(name, itemID, size)
		self._lower = lower
		self._upper = upper 
	
	def getLower(self):
		return self._lower
	
	def getUpper(self):
		return self._upper
	
	def foundIn(self, security):
		return (security >= self.getLower() and security <= higher)

ORES = {
	"plagioclase"			: Ore("Plagioclase", 18, 0.35),
	"rich plagioclase"		: Ore("Rich Plagioclase", 17456, 0.35), 
	"azure plagioclase"		: Ore("Azure Plagioclase", 17455, 0.35),
	"scordite"				: Ore("Scordite", 1228, 0.15),
	"condensed scordite"	: Ore("Condensed Scordite", 17463, 0.15),
	"massive scordite"		: Ore("Massive Scordite", 17464, 0.15),
	"pyroxeres"				: Ore("Pyroxeres", 1224, 0.3),
	"solid pyroxeres"		: Ore("Solid Pyroxeres", 17459, 0.3),
	"viscous pyroxeres"		: Ore("Viscous Pyroxeres", 17460, 0.3),
	"veldspar"				: Ore("Veldspar", 1230, 0.1),
	"dense veldspar"		: Ore("Dense Veldspar", 17471, 0.1),
	"concentrated veldspar"	: Ore("Concentrated Veldspar", 17470, 0.1),
}
"""
	"omber"					: Ore("Omber", 1227, 0.6, upper=0.7),
	"golden omber"			: Ore("Golden Omber", 17868, 0.6, upper=0.7),
	"silvery omber"			: Ore("Silvery Omber", 17867, 0.6, upper=0.7),
	"jaspet"				: Ore("Jaspet", 1226, 2.0, upper=0.4),
	"pure jaspet"			: Ore("Pure Jaspet", 17448, 2.0, upper=0.4),
	"pristine jaspet"		: Ore("Pristine Jaspet", 17449, 2.0, upper=0.4),
	"hedbergite"			: Ore("Hedbergite", 21, 3.0, upper=0.2),
	"glazed hedbergite"		: Ore("Glazed Hedbergite", 17441, 3.0, upper=0.2),
	"vitric hedbergite"		: Ore("Vitric Hedbergite", 17440, 3.0, upper=0.2),
	"kernite"				: Ore("Kernite", 20, 1.2, upper=0.7),
	"fiery kernite"			: Ore("Fiery Kernite", 17453, 1.2, upper=0.7),
	"luminous kernite"		: Ore("Luminous Kernite", 17452, 1.2, upper=0.7),
"""

def ores():
	return ORES.values()

def oreNames():
	return [ore.getName() for ore in ores()]

def find(name, exact=True):
	return util.dictFind(ORES, name, exact)

def oreValue(name, pricePerUnit, volume=1.0):
	try:
		ore = ORES[name]
	except KeyError:
		raise Exception("No ore named %s" % name)
	return ore.value(pricePerUnit, volume)

