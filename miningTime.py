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

import eve.ore
import eve.regions
import eve.market
import argparse
import sys

progDescription = """
Displays information about asteroids and mining.
"""

parser = argparse.ArgumentParser(description=progDescription)
parser.add_argument("-r", "--region", help="Regions to use in price lookup. Default is \"The Forge\"", default="The Forge")
parser.add_argument("-s", help="Skip market lookup", action="store_false", dest="lookup")
parser.add_argument("-e","--exact", help="Match ore name exactly. Note that matches--even exact--are ALWAYS case insensitive", action="store_true")
parser.add_argument("-m", help="Specify an ammount in m3. Displays units of ore mined instead of m3", action="store_true", dest="specify_meters") 
parser.add_argument("ore", help="Ore being mined")
parser.add_argument("size", help="Size of the asteroid (units)", type=float)
parser.add_argument("rate", help="Ore mined per cycle (m3)", nargs='?', type=float, default=0.0)
parser.add_argument("cycleTime", help="Cycle time (default 60)", nargs='?', type=float, default=60.0)
args = parser.parse_args()

def timeString(seconds):
	hours = seconds / 3600
	seconds = seconds % 3600
	minutes = seconds / 60
	seconds = seconds % 60
	return "%.2d:%.2d:%.2d" % (hours, minutes, seconds)

def main():
	oreName = args.ore
	exact = args.exact
	sizeInMeters = args.specify_meters
	asteroidSize = args.size
	rate = args.rate
	cycle = args.cycleTime
	region = args.region
	doMarketLookup = args.lookup
	ores = eve.ore.find(oreName, exact=exact)
	regions = eve.regions.find(region)
	marketStats = None
	if not ores:
		sys.stderr.write("No ore found for %s\n" % oreName)
		return
	if doMarketLookup:
		marketStats = eve.market.query(ores, regions=regions)
	for ore in ores:
		l = []
		name = ore.getName()
		l.append(name)
		oreSize = ore.getSize()
		if sizeInMeters:
			m3 = asteroidSize
			sizeInUnits = asteroidSize / oreSize
			l.append("%d units" % sizeInUnits)
		else:
			m3 = asteroidSize * oreSize
			sizeInUnits = asteroidSize
			l.append("%.2f m3" % m3)
		if doMarketLookup:
			oreStats = marketStats[ore].getBuyStats()
			pricePerUnit = oreStats.getPercentile()
			l.append("%.2f ISK (@ %.2f)" % (pricePerUnit * sizeInUnits, pricePerUnit))
		if rate > 0.0:
			timeToEmpty = m3/rate * cycle 
			l.append(timeString(timeToEmpty))
		print "\t".join(l)

if __name__ == "__main__":
	main()
