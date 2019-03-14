import copy

class SignalObject(object):
	"""docstring for SignalObject"""
	startbyte = 0
	startbit = 0
	length = 0
	value = 0
	
	#Constructor
	def __init__(self, startbyte, startbit, length, value):
		self.startbyte = startbyte
		self.startbit = startbit
		self.length = length
		self.value = value	

	def copy(self):
	# return SignalObject(self.startbyte, self.startbit, self.length, self.value)
		return SignalObject(copy.copy(self.startbyte), copy.copy(self.startbit), copy.copy(self.length), copy.copy(self.value))
