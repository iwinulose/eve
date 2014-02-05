def dictFind(dictionary, name, exact=True):
	lowerName = name.lower()
	result = []
	if exact:
		try:
			result.append(dictionary[lowerName])
		except KeyError:
			pass
	else:
		for key in dictionary:
			if lowerName in key:
				result.append(dictionary[key])
	return result

def isIter(obj):
	try:
		iter(obj)
		return True
	except:
		return False

def getIDs(items):
	if isIter(items):
		return map(lambda item: item.getID(), items)
	else:
		return [items.getID()]

