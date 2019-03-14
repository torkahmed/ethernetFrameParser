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

#
# HELPER FUNCTIONS
#
def filterHexToBin(hexDump):
	spaces = ' '
	outputBinary = ""
	outputDump = ""
	foundOnes = 0

	for char in hexDump:
		if char not in spaces:
			outputDump = outputDump + char
			
			#Adding Left 0s
			if (char == '0') & (foundOnes == 0):
				outputBinary = "0000" + outputBinary
				print "Added 0s"
			else:
				foundOnes = 1
				print "Found nonzero"
				pass
			pass
		pass
	pass
	print "Filtered hexDump = %s" % (outputDump)

	outputBinary = outputBinary + bin(int(outputDump, 16))[2:]

	print "Filtered Bin = %s with length %s" % (outputBinary, len(outputBinary))

	return outputBinary



#define start bytes/bits for all signals. TODO: read from DFL file
listOfSignals = []
signalX = SignalObject(0,0,8,0)

signalX.startbyte = 0
signalX.startbit = 0
signalX.length = 8
listOfSignals.append(signalX.copy())
print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)

signalX.startbyte = 1
signalX.startbit = 0
signalX.length = 16
listOfSignals.append(signalX.copy())
print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)

signalX.startbyte = 3
signalX.startbit = 0
signalX.length = 8
listOfSignals.append(signalX.copy())
print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)

signalX.startbyte = 4
signalX.startbit = 0
signalX.length = 32
listOfSignals.append(signalX.copy())
print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)


#get hex dump, TODO: import from wireshark, and filter to this format
#This hex dump needs to be in this format, big endian, hex values, discarding PDU and frame headers
hexDump = "00 ab cd dd fe ff df dd 12 31"

BinaryStream = filterHexToBin(hexDump)

print "First Element:: SB %s Sb %s Length %s Value %s" % (listOfSignals[0].startbyte, listOfSignals[0].startbit, listOfSignals[0].length, listOfSignals[0].value) 

# Get Signal Values from Byte Stream
for signal in listOfSignals:
	print "Sig SB: %s, Sb: %s" % (signal.startbyte, signal.startbit)
	index = (signal.startbyte * 8) + signal.startbit
	signal.value = BinaryStream[index : (index + signal.length)]
	print "Signal value: %s " % (signal.value)
	pass