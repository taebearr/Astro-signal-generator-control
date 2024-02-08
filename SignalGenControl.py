# ----------------------------------------------------------------------
# Name          : Initial Draft (Signal Generator).py
# Description   : To connect Terminal Mode (PC) with Signal Generator
# ----------------------------------------------------------------------
#Import Global Library
import socket
import time
import struct
import sys
import binascii
import os

from xml.dom import minidom

class AstroSG:
	def __init__(self):
		# Create socket object with UDP (Datagram)
		self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print("=== Initializing Socket ===\n\n")

		# Get sockaddr
		self.udpsockaddr = socket.getnameinfo(sockAddr, socket.NI_NUMERICSERV)

		print("=== Getting Socket Address & Port Num === ")
		print(self.udpsockaddr)
	
	def udpconnect(self):
		print('\n\n======= Connecting =======')
		stringmsg = chr(0x05)
		bytemsg = stringmsg.encode("cp1252")
		
		# sendto() is syntax for UDP
		self.udpsock.sendto(bytemsg, (sockAddr))
		
		print("\nMessage Sent : ", bytemsg, "\n")
		
		time.sleep(1)
		
		
	def udpdisconnect(self):
		stringmsg = chr(0x04)
		bytemsg = stringmsg.encode('cp1252')
		
		self.udpsock.sendto(bytemsg, (sockAddr))
		self.udpsock.close()
		
		print("\nMessage Sent : ", bytemsg, "\n")
		print('======= Disconnected =======')
		
	def printDebugLog(self, progNum, stringmsg, bytemsg):
		#Debugging purposes
		print("\n [ Prog Num ] : ", progNum)

		print("\n [ String Message Sent ] : ", stringmsg)
			
		print("\n [Byte Message Sent ] : ", bytemsg)

		
	def setProgNum(self, progNum):
		param = []
		progNum = [int(i) for i in str(progNum)]
		
		if len(progNum) == 4:
			for x in range(len(progNum)):
				string = ("3"+str(progNum[x]))
				an_integer = int(string, 16)
				param.append(an_integer)

			msglist = [0x02, 0xfd, 0x24, 0x20, param[0], param[1], param[2], param[3], 0x2c, 0x31, 0x03]

			# Join msglist as an ascii string
			stringmsg = ''.join(chr(i) for i in msglist)
			
			# Convert ascii to bytes
			bytemsg = stringmsg.encode('cp1252')
			
			self.udpsock.sendto(bytemsg, (sockAddr))
			
			self.printDebugLog(progNum, stringmsg, bytemsg)

		elif len(progNum) == 3:
			for x in range(len(progNum)):
				string = ("3"+str(progNum[x]))
				an_integer = int(string, 16)
				param.append(an_integer)

			msglist = [0x02, 0xfd, 0x24, 0x20, 0x30, param[0], param[1], param[2], 0x2c, 0x31, 0x03]

			# Join msglist as an ascii string
			stringmsg = ''.join(chr(i) for i in msglist)
			
			# Convert ascii to bytes
			bytemsg = bytes(stringmsg, 'cp1252')
			
			self.udpsock.sendto(bytemsg, (sockAddr))
			
			self.printDebugLog(progNum, stringmsg, bytemsg)	
		else:
			print("Error!! Program Number", progNum, "is wrong \n")
			sys.exit()
			
	def setPatternTiming(self, progNum):
		param = []
		progNum = [int(i) for i in str(progNum)]
		
		#add error handling
		if len(progNum) == 4:
			for x in range(len(progNum)):
				string = ("3"+str(progNum[x]))
				an_integer = int(string, 16)
				param.append(an_integer)

			msglist = [0x02, 0xfd, 0x24, 0x20, param[0], param[1], param[2], param[3], 0x2c, 0x32, 0x03]

			# Join msglist as an ascii string
			stringmsg = ''.join(chr(i) for i in msglist)
			
			# Convert ascii to bytes
			bytemsg = stringmsg.encode('cp1252')
			
			self.udpsock.sendto(bytemsg, (sockAddr))
			
			self.printDebugLog(progNum, stringmsg, bytemsg)			
			

# Astro SG
SG_ADDR  = "192.168.122.56"
SG_PORT  = 8000

sockAddr = (SG_ADDR, SG_PORT)
astroSG = AstroSG()
astroSG.setProgNum("1003")
astroSG.setPatternTiming("1127")

time.sleep(2)

response = input("\n\nInput 'e' to exit:\n")

# To exit program
if(response == "e"):
	astroSG.udpdisconnect()