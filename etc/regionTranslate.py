import sys

if __name__ == "__main__":
	print "REGIONS = {"
	for line in sys.stdin:
		tokens = line.split()
		regionId = int(tokens[0])
		regionComponents = tokens[1:]
		regionName = " ".join(regionComponents)
		regionLower = regionName.lower()
		print "\t\"%s\"\t:\tRegion(\"%s\", %d)," % (regionLower, regionName, regionId)
	print "}"

