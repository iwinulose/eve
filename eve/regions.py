# Copyright (c) 2014, Charles Duyk
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


from objects import Entity
import util

class Region(Entity):
	def __init__(self, name, theID):
		super(Region, self).__init__(name, theID)
		self._planets = []
		self._belts = []
		self._stations = []
		self._gates = []
	
	def getPlanets(self):
		return tuple(self._planets)
	
	def getBelts(self):
		return tuple(self._belts)
	
	def getStations(self):
		return tuple(self._stations)
	
	def getGates(self):
		return tuple(self._gates)

class Planet(Entity):
	def __init__(self, name, id):
		super(Planet, self).__init__(name, id)
	
REGIONS = {
	"aridia"	:	Region("Aridia", 10000054),
	"black rise"	:	Region("Black Rise", 10000069),
	"branch"	:	Region("Branch", 10000055),
	"cache"	:	Region("Cache", 10000007),
	"catch"	:	Region("Catch", 10000014),
	"cloud ring"	:	Region("Cloud Ring", 10000051),
	"cobalt edge"	:	Region("Cobalt Edge", 10000053),
	"curse"	:	Region("Curse", 10000012),
	"deklein"	:	Region("Deklein", 10000035),
	"delve"	:	Region("Delve", 10000060),
	"derelik"	:	Region("Derelik", 10000001),
	"detorid"	:	Region("Detorid", 10000005),
	"devoid"	:	Region("Devoid", 10000036),
	"domain"	:	Region("Domain", 10000043),
	"esoteria"	:	Region("Esoteria", 10000039),
	"essence"	:	Region("Essence", 10000064),
	"etherium reach"	:	Region("Etherium Reach", 10000027),
	"everyshore"	:	Region("Everyshore", 10000037),
	"fade"	:	Region("Fade", 10000046),
	"feythabolis"	:	Region("Feythabolis", 10000056),
	"fountain"	:	Region("Fountain", 10000058),
	"geminate"	:	Region("Geminate", 10000029),
	"genesis"	:	Region("Genesis", 10000067),
	"great wildlands"	:	Region("Great Wildlands", 10000011),
	"heimatar"	:	Region("Heimatar", 10000030),
	"immensea"	:	Region("Immensea", 10000025),
	"impass"	:	Region("Impass", 10000031),
	"insmother"	:	Region("Insmother", 10000009),
	"kador"	:	Region("Kador", 10000052),
	"khanid"	:	Region("Khanid", 10000049),
	"kor-azor"	:	Region("Kor-Azor", 10000065),
	"lonetrek"	:	Region("Lonetrek", 10000016),
	"malpais"	:	Region("Malpais", 10000013),
	"metropolis"	:	Region("Metropolis", 10000042),
	"molden heath"	:	Region("Molden Heath", 10000028),
	"oasa"	:	Region("Oasa", 10000040),
	"omist"	:	Region("Omist", 10000062),
	"outer passage"	:	Region("Outer Passage", 10000021),
	"outer ring"	:	Region("Outer Ring", 10000057),
	"paragon soul"	:	Region("Paragon Soul", 10000059),
	"period basis"	:	Region("Period Basis", 10000063),
	"perrigen falls"	:	Region("Perrigen Falls", 10000066),
	"placid"	:	Region("Placid", 10000048),
	"providence"	:	Region("Providence", 10000047),
	"pure blind"	:	Region("Pure Blind", 10000023),
	"querious"	:	Region("Querious", 10000050),
	"scalding pass"	:	Region("Scalding Pass", 10000008),
	"sinq laison"	:	Region("Sinq Laison", 10000032),
	"solitude"	:	Region("Solitude", 10000044),
	"stain"	:	Region("Stain", 10000022),
	"syndicate"	:	Region("Syndicate", 10000041),
	"tash-murkon"	:	Region("Tash-Murkon", 10000020),
	"tenal"	:	Region("Tenal", 10000045),
	"tenerifis"	:	Region("Tenerifis", 10000061),
	"the bleak lands"	:	Region("The Bleak Lands", 10000038),
	"the citadel"	:	Region("The Citadel", 10000033),
	"the forge"	:	Region("The Forge", 10000002),
	"the kalevala expanse"	:	Region("The Kalevala Expanse", 10000034),
	"the spire"	:	Region("The Spire", 10000018),
	"tribute"	:	Region("Tribute", 10000010),
	"vale of the silent"	:	Region("Vale of the Silent", 10000003),
	"venal"	:	Region("Venal", 10000015),
	"verge vendor"	:	Region("Verge Vendor", 10000068),
	"wicked creek"	:	Region("Wicked Creek", 10000006),
}

def regions():
	return REGIONS.values()

def find(name, exact=True):
	return util.dictFind(REGIONS, name, exact)
