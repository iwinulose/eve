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

