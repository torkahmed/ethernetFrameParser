from copy import copy
import signalObject

#
# MACROS
#
DEBUG = 1
PDU_HDR_LEN = 8
WIRESHARK_HEXDUMP = "wiresharkHexDump.txt"
FRAME_DBC = "dbc.txt"

#
# HELPER FUNCTIONS
#


def parseWiresharkHexDump(listOfSignals):
	# This function parses a wireshark hex dump
	outputHexdump = ""

	f = open(WIRESHARK_HEXDUMP, "r")
	hexdump = f.read()
	hexdump = hexdump.split(" ")

	for element in hexdump:
		if len(element) == 2:
			outputHexdump = outputHexdump + copy(element)
			pass
		pass

	return outputHexdump


#DUMMYFUNC
def fillListOfSignals(listOfSignals):

	signalX = signalObject.SignalObject("test", 0,0,8,0)
	
	#TODO: Get data from DBC
	signalX.name = "PDU_HDR"
	signalX.startbyte = 0
	signalX.startbit = 0
	signalX.length = 64
	listOfSignals.append(signalX.copy())

	signalX.name = "SIGNAL1"
	signalX.startbyte = 0 + PDU_HDR_LEN
	signalX.startbit = 0
	signalX.length = 10
	listOfSignals.append(signalX.copy())
	if DEBUG == 1:
		print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)

	signalX.name = "SIGNAL2"
	signalX.startbyte = 1 + PDU_HDR_LEN
	signalX.startbit = 0
	signalX.length = 13
	listOfSignals.append(signalX.copy())
	if DEBUG == 1:
		print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)

	signalX.name = "SIGNAL3"
	signalX.startbyte = 3 + PDU_HDR_LEN
	signalX.startbit = 0
	signalX.length = 2
	listOfSignals.append(signalX.copy())
	if DEBUG == 1:
		print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)

	signalX.name = "SIGNAL4"
	signalX.startbyte = 4 + PDU_HDR_LEN
	signalX.startbit = 0
	signalX.length = 35
	listOfSignals.append(signalX.copy())
	if DEBUG == 1:
		print "Incrementing Signal with SB %s and Sb %s and length %s" % (signalX.startbyte, signalX.startbit, signalX.length)	
	pass


def getSignalInfoFromDBC(listOfSignals):
	# Function parses the doc file to understand the signal startbytes, bits, etc.
	#TODO: Save multiple frames in array of objects based on frame_done increment
	#TODO: Account for frame header, right now the assumption is that only the frame payload is being parsed

	# Indication to which frame is being parsed.
	frameOpened = False
	# Signal absolute offset from the start of the frame payload
	absoluteOffset = 0
	# Accumulated Offset in the current PDU, added to absolute offset at the end of the PDU, then cleared to be re-used
	pduOffset = 0


	signalX = signalObject.SignalObject("test", 0,0,8,0)


	with open(FRAME_DBC) as f:
		for line in f:
			#print line
			if "frame " in line:
				frameLine = line.split()
				if DEBUG == 1:
					print "Start of Frame: %s" % frameLine[1]
				frameOpened = frameLine[1]

			if ("pdu " in line) and (frameOpened != False):
				pduLine = line.split()
				if DEBUG == 1:
					print "Start of PDU %s in frame %s" % (pduLine[1], frameOpened)
				signalX.name = pduLine[1] + "_HDR"
				signalX.startbyte = absoluteOffset
				signalX.startbit = 0
				signalX.length = 64
				listOfSignals.append(signalX.copy())
				absoluteOffset = absoluteOffset + 8


			if ("signal " in line)  and (frameOpened != False):
				signalLine = line.split()
				if DEBUG == 1:
					print "Signal Detected %s in frame %s with StartByte %s, Startbit %s, Length %s" % (signalLine[1], frameOpened, signalLine[2], signalLine[3], signalLine[4])
				signalX.name = signalLine[1]
				signalX.startbyte = int(signalLine[2]) + absoluteOffset
				signalX.startbit = int(signalLine[3])
				signalX.length = int(signalLine[4])
				listOfSignals.append(signalX.copy())

				# Adding PDU Offset  (startbyte * 8)  +    startbit        +        length     -- In Bytes
				pduOffset = ((int(signalLine[2]) * 8) + int(signalLine[3]) + int(signalLine[4])) / 8

			if ("pdu_done" in line) and (frameOpened != False):
				print "PDU Done, Adding PDU Offset %s to Absolute %s" % (pduOffset, absoluteOffset)
				absoluteOffset = absoluteOffset + pduOffset
				pduOffset = 0

			if ("frame_done" in line) and (frameOpened != False):
				if DEBUG == 1:
					print "End of Frame %s, Exiting Function" % frameOpened
				frameOpened = False
				break

	return

#DUMMYFUNC
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
		print "[%s] %s = decimal (%s) , hex (%s) , binary (%s)" % (idx, signal.name, int(signal.value, 2) , hex(int(signal.value, 2)) , signal.value)
	print "#############################"
	print "#############################"
#
# MAIN
#

#define start bytes/bits for all signals. TODO: read from DFL file
listOfSignals = []

getSignalInfoFromDBC(listOfSignals)

#fillListOfSignals(listOfSignals)

# hexDump = getHexDump()
hexDump = parseWiresharkHexDump(listOfSignals)

BinaryStream = filterHexToBin(hexDump)

# Get Signal Values from Byte Stream
evaluateSignalValues(listOfSignals)
# Print Values
printSignals(listOfSignals)