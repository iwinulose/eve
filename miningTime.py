#!/usr/bin/env python
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
