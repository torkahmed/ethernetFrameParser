import copy

class SignalObject(object):
	"""docstring for SignalObject"""
	name = "no_name"
	startbyte = 0
	startbit = 0
	length = 0
	value = 0
	
	#Constructor
	def __init__(self, name, startbyte, startbit, length, value):
		self.name = name
		self.startbyte = startbyte
		self.startbit = startbit
		self.length = length
		self.value = value	

	def copy(self):
		return SignalObject(copy.copy(self.name), copy.copy(self.startbyte), copy.copy(self.startbit), copy.copy(self.length), copy.copy(self.value))