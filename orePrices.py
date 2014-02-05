#!/usr/bin/env python
import sys
import argparse
import eve.ore
import eve.market
import eve.regions

progDescription = """
Fetches market data from eve-central and prints out a list of ore
values per m3. 
"""

def main(args):
	region = args.region
	ores = eve.ore.ores()
	regions = eve.regions.find(region)
	marketResults = eve.market.query(ores, regions=regions)
	showSell = args.sell
	showPerUnit = args.unit_price
	l = []
	for ore in marketResults:
		result = marketResults[ore]
		name = ore.getName()
		if showSell:
			marketStats = result.getSellStats()
		else:
			marketStats = result.getBuyStats()
		pricePerUnit = marketStats.getPercentile()
		pricePerM3 = ore.valueByVolume(pricePerUnit)
		price = pricePerUnit if showPerUnit else pricePerM3
		l.append((name, price))
	l.sort(key=lambda tup: tup[1], reverse=True)
	strings = map(lambda tup: "%s %.2f" % (tup[0], tup[1]), l)
	print "\n".join(strings)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=progDescription)
	parser.add_argument("-r", "--region", help="Regions to use in price lookup. Default is \"The Forge\"", default="The Forge")
	parser.add_argument("-a", "--all", help="Shows more information about the ores.", action="store_true")
	parser.add_argument("-s", "--sell", help="Show sell order prices (default buy orders)", action="store_true")
	parser.add_argument("-u", "--unit-price", help="Show price per unit, not per m3", action="store_true")
	args = parser.parse_args()
	main(args)
