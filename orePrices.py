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

PRICE_TYPE_PERCENTILE = "percentile"
PRICE_TYPE_AVERAGE = "average"
PRICE_TYPE_MIN = "min" 
PRICE_TYPE_MAX = "max"
PRICE_TYPE_DEFAULT = PRICE_TYPE_PERCENTILE

ORDER_TYPE_BUY = "buy"
ORDER_TYPE_SELL = "sell"
ORDER_TYPE_DEFAULT = ORDER_TYPE_BUY


def get_unit_price(result, order_type=ORDER_TYPE_DEFAULT, price_type=PRICE_TYPE_DEFAULT):
	market_stats = None
	price = 0.0
	if order_type == ORDER_TYPE_BUY:
		market_stats = result.getBuyStats()
	elif order_type == ORDER_TYPE_SELL:
		market_stats = result.getSellStats()
	else:
		raise ValueError("Invalid order type {}".format(order_type))
	if price_type == PRICE_TYPE_PERCENTILE:
		price = market_stats.getPercentile()
	elif price_type == PRICE_TYPE_AVERAGE:
		price = market_stats.getAverage()
	elif price_type == PRICE_TYPE_MIN:
		price = market_stats.getMin()
	elif price_type == PRICE_TYPE_MAX:
		price = market_stats.getMax()
	else:
		raise ValueError("Invalid price type {}".format(price_type))
	return price
	

def main(args):
	region = args.region
	ores = eve.ore.ores()
	regions = eve.regions.find(region)
	marketResults = eve.market.query(ores, regions=regions)
	showPerUnit = args.unit_price
	l = []
	for ore in marketResults:
		result = marketResults[ore]
		name = ore.getName()
		pricePerUnit = get_unit_price(result, args.order_type, args.price_type)
		pricePerM3 = ore.valueByVolume(pricePerUnit)
		price = pricePerUnit if showPerUnit else pricePerM3
		l.append((name, price))
	l.sort(key=lambda tup: tup[1], reverse=True)
	strings = map(lambda tup: "%s %.2f" % (tup[0], tup[1]), l)
	print "\n".join(strings)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=progDescription)
	parser.add_argument("-r", "--region", 
		default="The Forge", 
		help="Regions to use in price lookup. Default is \"The Forge\"")
	parser.add_argument("-u", "--unit-price", 
		action="store_true", 
		help="Show price per unit")
	order_type_group = parser.add_mutually_exclusive_group()
	order_type_group.add_argument("-b", "--buy", 
		dest="order_type", 
		action="store_const", 
		default=ORDER_TYPE_DEFAULT, 
		const=ORDER_TYPE_BUY, 
		help="Show buy orders (default)")
	order_type_group.add_argument("-s", "--sell", 
		dest="order_type",
		action="store_const", 
		const=ORDER_TYPE_SELL, 
		help="Show sell orders")
	price_type_group = parser.add_mutually_exclusive_group()
	price_type_group.add_argument("--percentile", 
		dest="price_type",
		action="store_const",
		const=PRICE_TYPE_PERCENTILE,
		default=PRICE_TYPE_DEFAULT,
		help="Show highest 5% of buy orders, or lowest 5% of sell orders (default)")
	price_type_group.add_argument("--min", 
		dest="price_type",
		action="store_const",
		const=PRICE_TYPE_MIN,
		help="Show minimum prices")
	price_type_group.add_argument("--max", 
		dest="price_type",
		action="store_const",
		const=PRICE_TYPE_MAX,
		help="Show maximum prices")
	price_type_group.add_argument("--average", "--avg",
		dest="price_type",
		action="store_const",
		const=PRICE_TYPE_AVERAGE,
		help="Show average prices")
	args = parser.parse_args()
	main(args)
