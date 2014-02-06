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

import util
import requests
from xml.etree import ElementTree
from requests import RequestException

class MarketError(Exception):
	pass

class MarketStatistics(object):
	def __init__(self, xml=None, minimum=0.0, maximum=0.0, average=0.0, median=0.0, stddev=0.0, percentile=0.0, volume=0):
		if xml is not None:
			minElem = xml.find("./min")
			maxElem = xml.find("./max")
			avgElem = xml.find("./avg")
			medianElem = xml.find("./median")
			stddevElem = xml.find("./stddev")
			percentileElem = xml.find("./percentile")
			volumeElem = xml.find("./volume")
			minimum = float(minElem.text)
			maximum = float(maxElem.text)
			average = float(avgElem.text)
			median = float(medianElem.text)
			stddev = float(stddevElem.text)
			percentile = float(percentileElem.text)
			volume = int(volumeElem.text)
		self._min = minimum
		self._max = maximum
		self._average = average
		self._median = median
		self._stddev = stddev
		self._percentile = percentile
		self._volume = volume
	
	def __repr__(self):
		return "MarketStatistics(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %d)" % (self.getMin(), self.getMax(), self.getAverage(), self.getMedian(), self.getStddev(), self.getPercentile(), self.getVolume())
	
	def __str__(self):
		return "min: %.2f max: %.2f avg: %.2f median: %.2f stddev: %.2f percentile: %.2f volume: %d" % (self.getMin(), self.getMax(), self.getAverage(), self.getMedian(), self.getStddev(), self.getPercentile(), self.getVolume())
	
	def getMin(self):
		return self._min
	
	def getMax(self):
		return self._max
	
	def getAverage(self):
		return self._average
	
	def getMedian(self):
		return self._median
	
	def getStddev(self):
		return self._stddev
	
	def getPercentile(self):
		return self._percentile
	
	def getVolume(self):
		return self._volume

class MarketResults(object):
	def __init__(self, xml=None, buyStats=None, sellStats=None, allStats=None):
		if xml is not None:
			buyElem = xml.find("./buy")
			sellElem = xml.find("./sell")
			allElem = xml.find("./all")
			buyStats = MarketStatistics(xml=buyElem)
			sellStats = MarketStatistics(xml=sellElem)
			allStats = MarketStatistics(xml=allElem)
		self._buyStats = buyStats
		self._sellStats = sellStats
		self._allStats = allStats
	
	def getBuyStats(self):
		return self._buyStats
	
	def getSellStats(self):
		return self._sellStats
	
	def getAllStats(self):
		return self._allStats
	
	def __repr__(self):
		buy = repr(self.getBuyStats())
		sell = repr(self.getSellStats())
		all = repr(self.getAllStats())
		return "MarketResults({}, {}, {})".format(buy, sell, all)
	
	def __str__(self):
		return "Market Results:\nbuy: {}\nsell: {}\nall: {}".format(self.getBuyStats(), self.getSellStats(), self.getAllStats())

def parseResults(text):
	root = ElementTree.XML(text)
	items = root.findall(".//type")
	results = {}
	for itemElem in items:
		itemID = int(itemElem.attrib["id"])
		result = MarketResults(xml=itemElem)
		results[itemID] = result
	return results

def query(items, hours=24, regions=None, system=None, minQuantity=0):
	if not items:
		raise MarketError("No items to query")
	itemIDs = util.getIDs(items)
	idsToItemsDict = dict(zip(itemIDs, items))
	regionIDs = None
	systemID = None
	if regions:
		regionIDs = util.getIDs(regions)
	if system:
		systemID = system.getID()
	endpoint = "http://api.eve-central.com/api/marketstat"
	params = {}
	params["typeid"] = itemIDs
	params["hours"] = hours
	if regionIDs:
		params["regionlimit"] = regionIDs
	if systemID:
		params["usesystem"] = systemID
	if minQuantity > 0:
		params["minQ"] = minQuantity
	try:
		response = requests.get(endpoint, params=params)
		response.raise_for_status()
	except RequestException as e:
		raise MarketError("Error fetching from eve-central", response, e)
	xmlText = response.text
	try:
		idsToResultsDict = parseResults(xmlText)
		itemsToResultsDict = {}
		for itemID in idsToResultsDict:
			item = idsToItemsDict[itemID]
			result = idsToResultsDict[itemID] 
			itemsToResultsDict[item] = result
	except Exception as e:
		raise MarketError("Error processing results", e)
	return itemsToResultsDict

if __name__ == "__main__":
	import ore
	import regions
	r = query(ore.ores(), regions=regions.find("the forge"))
	for k in r:
		print k.getName(), r[k]

