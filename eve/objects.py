class Entity(object):
	def __init__(self, name, theId):
		self._name = name
		self._id = int(theId)
	
	def __repr__(self):
		return "%s(\"%s\", %d)" % (self.__class__.__name__, self.getName(), self.getID())
	
	def __str__(self):
		return "%s (id: %d)" % (self.getName(), self.getID())
	
	def __eq__(self, other):
		if isinstance(other, Entity):
			return self.getID() == other.getID()
		return NotImplemented
	
	def __ne__(self, other):
		isEqual = self.__eq__(other)
		if isEqual is NotImplemented:
			return isEqual
		return not isEqual
	
	def getName(self):
		return self._name
	
	def getID(self):
		return self._id
	
	def valueByVolume(self, pricePerUnit, volume=1.0):
		volumeFloat = volume + 0.0
		unitVolume = self.getSize()
		pricePerMeter = pricePerUnit/unitVolume
		value = pricePerMeter * volumeFloat
		return value
		

class Item(Entity):
	def __init__(self, name, marketID, size):
		super(Item, self).__init__(name, marketID)
		self._size = size + 0.0
	
	def __repr__(self):
		return "Item(\"%s\", %d, %f)" % (self.getName(), self.getID(), self.getSize())
	
	def __str__(self):
		return "%s: id %d size %f" % (self.getName(), self.getID(), self.getSize())
	
	def getSize(self):
		return self._size

