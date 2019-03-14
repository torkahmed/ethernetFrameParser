from copy import copy
import signalObject

#
# FEATURE SWITCHES
#
DEBUG = 0

#
# HELPER FUNCTIONS
#


def parseWiresharkHexDump(listOfSignals):
	# This function parses a wireshark hex dump
	outputHexdump = ""

	f = open("wiresharkHexDump.txt", "r")
	hexdump = f.read()
	hexdump = hexdump.split(" ")

	for element in hexdump:
		if len(element) == 2:
			outputHexdump = outputHexdump + copy(element)
			pass
		pass

	return outputHexdump

def fillListOfSignals(listOfSignals):

	signalX = signalObject.SignalObject("test", 0,0,8,0)
	
	#TODO: Get data from DBC
	signalX.name = "SIGNAL1"
	signalX.startbyte = 0
	signalX.startbit = 0
	signalX.length = 10
	listOfSignals.append(signalX.copy())
	if DEBUG == 1:
		print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)

	signalX.name = "SIGNAL2"
	signalX.startbyte = 1
	signalX.startbit = 0
	signalX.length = 13
	listOfSignals.append(signalX.copy())
	if DEBUG == 1:
		print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)

	signalX.name = "SIGNAL3"
	signalX.startbyte = 3
	signalX.startbit = 0
	signalX.length = 2
	listOfSignals.append(signalX.copy())
	if DEBUG == 1:
		print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)

	signalX.name = "SIGNAL4"
	signalX.startbyte = 4
	signalX.startbit = 0
	signalX.length = 35
	listOfSignals.append(signalX.copy())
	if DEBUG == 1:
		print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)	
	pass

def getHexDump():
	#get hex dump, TODO: import from wireshark, and filter to this format
	#This hex dump needs to be in this format, big endian, hex values, discarding PDU and frame headers
	hexDump = "00 ab cd dd fe ff df dd 12 31"
	return hexDump

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
				if DEBUG == 1:
					print "Added 0s"
			else:
				foundOnes = 1
				if DEBUG == 1:
					print "Found nonzero"
				pass
			pass
		pass
	pass
	if DEBUG == 1:
		print "Filtered hexDump = %s" % (outputDump)

	outputBinary = outputBinary + bin(int(outputDump, 16))[2:]

	if DEBUG == 1:
		print "Filtered Bin = %s with length %s" % (outputBinary, len(outputBinary))

	return outputBinary


def evaluateSignalValues(listOfSignals):
	for signal in listOfSignals:
		if DEBUG == 1:
			print "Sig SB: %s, Sb: %s" % (signal.startbyte, signal.startbit)
		index = (signal.startbyte * 8) + signal.startbit
		signal.value = BinaryStream[index : (index + signal.length)]
		if DEBUG == 1:
			print "Signal value: %s " % (signal.value)
		pass	


def printSignals(listOfSignals):
	print "#############################"
	print "#############################"
	for idx,signal in enumerate(listOfSignals):
		print "Signal[%s] with name %s has value %s (%s)" % (idx, signal.name, int(signal.value, 2) , signal.value)
	print "#############################"
	print "#############################"
#
# MAIN
#

#define start bytes/bits for all signals. TODO: read from DFL file
listOfSignals = []

fillListOfSignals(listOfSignals)

# hexDump = getHexDump()
hexDump = parseWiresharkHexDump(listOfSignals)

BinaryStream = filterHexToBin(hexDump)

# Get Signal Values from Byte Stream
evaluateSignalValues(listOfSignals)
# Print Values
printSignals(listOfSignals)