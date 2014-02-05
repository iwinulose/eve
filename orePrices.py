#!/usr/bin/env python
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
