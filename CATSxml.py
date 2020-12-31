import sys
import xml.etree.ElementTree as ET

##################################################################################################################
#
# XML Examples
#
##################################################################################################################
#
# BLOCKS
#
#<BLOCK NAME="block_name" STATION="station_name" DISCIPLINE="CTC" VISIBLE="true">
#  <OCCUPIEDSPEC>
#	<IOSPEC DECADDR="address" JMRIPREFIX="prefix" EXIT_CMD="true" USER_NAME="user_name">throw</IOSPEC>
#  </OCCUPIEDSPEC>
#  <UNOCCUPIEDSPEC>
#	<IOSPEC DECADDR="address" JMRIPREFIX="prefix" EXIT_CMD="true" USER_NAME="user_name">close</IOSPEC>
#  </UNOCCUPIEDSPEC>
#</BLOCK>
#
# SIGNALS
#
#<SECSIGNAL>
#  CTC OS Left IM-W-DWF
#  <PANELSIGNAL SIGLOCATION="UPCENT" SIGORIENT="LEFT" SIGPANTYPE="LAMP1" />
#  <PHYSIGNAL>
#	testbed single
#	<ASPECTTBL>
#	  <HEADSTATES SIGNALHEAD="CTC OS Left IM-W-DWF">
#		<ASPECTCOMMAND PLABEL="green">
#		  <IOSPEC DECADDR="2031" JMRIPREFIX="CT" EXIT_CMD="true" USER_NAME="CTC OS Left IM-W-DWF-GRN">throw</IOSPEC>
#		</ASPECTCOMMAND>
#		<ASPECTCOMMAND PLABEL="yellow">
#		  <IOSPEC DECADDR="2030" JMRIPREFIX="CT" EXIT_CMD="true" USER_NAME="CTC OS Left IM-W-DWF-YEL">throw</IOSPEC>
#		</ASPECTCOMMAND>
#		<ASPECTCOMMAND PLABEL="red">
#	  <IOSPEC DECADDR="2029" JMRIPREFIX="CT" EXIT_CMD="true" USER_NAME="CTC OS Left IM-W-DWF-RED">throw</IOSPEC>
#		</ASPECTCOMMAND>
#	  </HEADSTATES>
#	</ASPECTTBL>
#  </PHYSIGNAL>
#</SECSIGNAL>
#
# TURNOUTS
#
#<SWITCHPOINTS>
#  <ROUTEINFO ROUTEID="RIGHT" NORMAL="true">
#	 <SELECTEDREPORT>
#	   <IOSPEC DECADDR="2005" JMRIPREFIX="CS" EXIT_CMD="true" USER_NAME="CTC OS Left TO">close</IOSPEC>
#	 </SELECTEDREPORT>
#	 <ROUTECOMMAND>
#	   <IOSPEC DECADDR="2" JMRIPREFIX="NT" EXIT_CMD="true" USER_NAME="CTC OS Left TO">close</IOSPEC>
#	 </ROUTECOMMAND>
#	 </ROUTEINFO>
#	   <ROUTEINFO ROUTEID="TOP">
#	 <SELECTEDREPORT>
#	   <IOSPEC DECADDR="2006" JMRIPREFIX="CS" EXIT_CMD="true" USER_NAME="CTC OS Left TO">throw</IOSPEC>
#	 </SELECTEDREPORT>
#	 <ROUTECOMMAND>
#	   <IOSPEC DECADDR="2" JMRIPREFIX="NT" EXIT_CMD="true" USER_NAME="CTC OS Left TO">throw</IOSPEC>
#	 </ROUTECOMMAND>
#  </ROUTEINFO>
#</SWITCHPOINTS>
##################################################################################################################
#
# XML Functions
#
##################################################################################################################
class CATSxml:
	#
	# Constructor
	#
	def __init__(self, name):
		self.mCATSName = name
		self.mXmlTemplateFile = "CATSTemplates/%s.xml" % name
		self.mXmlOutputFile = "%s.xml" % name
		self.mXmlTree = None
		self.mXmlRoot = None
		self.mXOffset = 0
		self.mYOffset = 0
		self.mNumRows = 0
		self.mNumCols = 0
	pass
	#
	# section offset functions
	#
	def GetSize(self):
		return [self.mNumCols, self.mNumRows]
	pass
	def SetXOffset(self, offset):
		self.mXOffset = offset
	pass
	def SetYOffset(self, offset):
		self.mYOffset = offset
	pass	
	#
	# Read the XML template file and get attached to the root
	#
	def Read(self):
		print("Reading XML File: %s..." % self.mXmlTemplateFile)
		self.mXmlTree = ET.parse(self.mXmlTemplateFile)
		self.mXmlRoot = self.mXmlTree.getroot()
	pass
	#
	# Write the XML file and get attached to the root
	#
	def Write(self):
		if (self.mXmlTree != None):
			print("Writing XML File: %s..." % self.mXmlOutputFile)
			self.mXmlTree.write(self.mXmlOutputFile)
		pass
	pass
	#
	# Debug Dump function
	#
	def DebugDump(self):
		ET.dump(self.mXmlRoot)
	pass
	#
	# Traverse the XML tree and find the node elements
	#
	def Print(self, cb_get_discipline, cb_get_block, cb_get_signal, cb_get_turnout):
		new_discipline = cb_get_discipline()
		for child in self.mXmlRoot:
			if (child.tag == "TRACKPLAN"):
				self.mNumCols = int(child.get('COLUMNS').replace("\n", ""))
				self.mNumRows = int(child.get('ROWS').replace("\n", ""))
				print("XML Track Plan %s (%d wide x %d high) Contains:" % (self.mCATSName, self.mNumCols, self.mNumRows))
				
				print("\tSECTIONS:")
				for section in child.iter('SECTION'):
					section_x = int(section.get('X').replace("\n", ""))
					section_y = int(section.get('Y').replace("\n", ""))
					print("\t\tSection @ (%d, %d)" % (section_x, section_y))
				pass
			
				print("\tBLOCKS:")
				for block in child.iter('BLOCK'):
					if (block.get('NAME') != None):
						block_name = block.get('NAME').replace("\n", "")
						block_disc = block.get('DISCIPLINE').replace("\n", "")
						if block_disc != "ABS":
							print("\t\tBLOCK: %s, DISCIPLINE = %s => %s" % (block_name, block_disc, new_discipline))
						for occupy in block.iter('OCCUPIEDSPEC'):
							for iospec in occupy.iter('IOSPEC'):
								block_pref = iospec.get('JMRIPREFIX').replace("\n", "")
								block_addr = iospec.get('DECADDR').replace("\n", "")
								block_user = iospec.get('USER_NAME').replace("\n", "")
								block_text = iospec.text
								new_pin    = cb_get_block(block_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									print("\t\t\tName = %30s, Prefix = %s => %s, Address = %s => %s, OCCUPIED   = %s = %s" % (block_user, block_pref, new_pref, block_addr, new_addr, block_text, new_text))
								else:
									print("\t\t\tName = %30s, Prefix = %s, Address = %s, OCCUPIED = %s" % (block_user, block_pref, block_addr, block_text))
								pass
							pass
						pass
						for unoccupy in block.iter('UNOCCUPIEDSPEC'):
							for iospec in unoccupy.iter('IOSPEC'):
								block_pref = iospec.get('JMRIPREFIX').replace("\n", "")
								block_addr = iospec.get('DECADDR').replace("\n", "")
								block_user = iospec.get('USER_NAME').replace("\n", "")
								block_text = iospec.text
								new_pin    = cb_get_block(block_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									if (new_text == "throw"):
										new_text = "close"
									pass
									print("\t\t\tName = %30s, Prefix = %s => %s, Address = %s => %s, UNOCCUPIED = %s => %s" % (block_user, block_pref, new_pref, block_addr, new_addr, block_text, new_text))
								else:
									print("\t\t\tName = %30s, Prefix = %s, Address = %s, UNOCCUPIED = %s" % (block_user, block_pref, block_addr, block_text))
								pass
							pass
						pass
					pass
				pass
				print("\tSIGNALS:")
				for head in child.iter('SECSIGNAL'):
					head_name = head.text
					head_name = head_name.replace("\n", "")
					head_name = head_name.lstrip()
					for aspect in head.iter('ASPECTCOMMAND'):
						head_color = aspect.get('PLABEL').replace("\n", "")
						for iospec in aspect.iter('IOSPEC'):
							head_pref = iospec.get('JMRIPREFIX').replace("\n", "")
							head_addr = iospec.get('DECADDR').replace("\n", "")
							head_user = iospec.get('USER_NAME').replace("\n", "")
							head_text = iospec.text
							print("\t\tHEAD: %s" % (head_user))
							new_pin = cb_get_signal(head_user)
							if (len(new_pin) == 3):
								new_pref = new_pin[0]
								new_addr = new_pin[1]
								new_text = new_pin[2]
								print("\t\t\tName = %30s, Prefix = %s => %s, Address = %s => %s, Lamp = %-s, Active = %s => %s" % (head_user, head_pref, new_pref, head_addr, new_addr, head_color, head_text, new_text))
							else:
								print("\t\t\tName = %30s, Prefix = %s, Address = %s, Lamp = %-s, Active = %s" % (head_user, head_pref, head_addr, head_color, head_text))
							pass
						pass
					pass
				pass
				print("\tTURNOUTS:")
				for switchpoint in child.iter('SWITCHPOINTS'):
					for points in switchpoint.iter('POINTSMSG'):
						for iospec in points.iter('IOSPEC'):
							pnt_pref = iospec.get('JMRIPREFIX').replace("\n", "")
							pnt_addr = iospec.get('DECADDR').replace("\n", "")
							pnt_user = iospec.get('USER_NAME').replace("\n", "")
							pnt_text = iospec.text
							new_pin  = cb_get_turnout(pnt_user)
							if (len(new_pin) == 3):
								new_pref = new_pin[0]
								new_addr = new_pin[1]
								new_text = new_pin[2]
								print("\t\t\t\t  Point Message: Name = %30s, Prefix = %s => %s, Address = %s => %s, Active = %s => %s" % (pnt_user, pnt_pref, new_pref, pnt_addr, new_addr, pnt_text, new_text))
							else:
								print("\t\t\t\t  Point Message: Name = %30s, Prefix = %s, Address = %s, Active = %s" % (pnt_user, pnt_pref, pnt_addr, pnt_text))
							pass
						pass
					pass
					
					for route in switchpoint.iter('ROUTEINFO'):
						print("\t\tTURNOUT:")
						route_id = route.get('ROUTEID').replace("\n", "")
						route_norm = route.get('NORMAL')
						if (route_norm == None):
							route_norm = "REVERSE"
						else:
							route_norm = "NORMAL"
						pass
						print("\t\t\t%s: %s" % (route_norm, route_id))
						for report in route.iter('SELECTEDREPORT'):
							for iospec in report.iter('IOSPEC'):
								rpt_pref = iospec.get('JMRIPREFIX').replace("\n", "")
								rpt_addr = iospec.get('DECADDR').replace("\n", "")
								rpt_user = iospec.get('USER_NAME').replace("\n", "")
								rpt_text = iospec.text
								new_pin	 = cb_get_turnout(rpt_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									print("\t\t\t\tSelected Report: Name = %30s, Prefix = %s => %s, Address = %s => %s, Active = %s => %s" % (rpt_user, rpt_pref, new_pref, rpt_addr, new_addr, rpt_text, new_text))
								else:
									print("\t\t\t\tSelected Report: Name = %30s, Prefix = %s, Address = %s, Active = %s" % (rpt_user, rpt_pref, rpt_addr, rpt_text))
								pass
							pass
						pass
						for report in route.iter('NOTSELECTEDREPORT'):
							for iospec in report.iter('IOSPEC'):
								rpt_pref = iospec.get('JMRIPREFIX').replace("\n", "")
								rpt_addr = iospec.get('DECADDR').replace("\n", "")
								rpt_user = iospec.get('USER_NAME').replace("\n", "")
								rpt_text = iospec.text
								new_pin	 = cb_get_turnout(rpt_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									print("\t\t\t\tUnselected Report: Name = %30s, Prefix = %s => %s, Address = %s => %s, Active = %s => %s" % (rpt_user, rpt_pref, new_pref, rpt_addr, new_addr, rpt_text, new_text))
								else:
									print("\t\t\t\tUnselected Report: Name = %30s, Prefix = %s, Address = %s, Active = %s" % (rpt_user, rpt_pref, rpt_addr, rpt_text))
								pass
							pass
						pass
						for command in route.iter('ROUTECOMMAND'):
							for iospec in command.iter('IOSPEC'):
								cmd_pref = iospec.get('JMRIPREFIX').replace("\n", "")
								cmd_addr = iospec.get('DECADDR').replace("\n", "")
								cmd_user = iospec.get('USER_NAME').replace("\n", "")
								cmd_text = iospec.text
								new_pin  = cb_get_turnout(cmd_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									print("\t\t\t\t  Route Command: Name = %30s, Prefix = %s => %s, Address = %s => %s, Active = %s => %s" % (cmd_user, cmd_pref, new_pref, cmd_addr, new_addr, cmd_text, new_text))
								else:
									print("\t\t\t\t  Route Command: Name = %30s, Prefix = %s, Address = %s, Active = %s" % (cmd_user, cmd_pref, cmd_addr, cmd_text))
								pass
							pass
						pass
						for request in route.iter('ROUTEREQUEST'):
							for iospec in request.iter('IOSPEC'):
								req_pref = iospec.get('JMRIPREFIX').replace("\n", "")
								req_addr = iospec.get('DECADDR').replace("\n", "")
								req_user = iospec.get('USER_NAME').replace("\n", "")
								req_text = iospec.text
								new_pin  = cb_get_turnout(req_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									print("\t\t\t\t  Route Request: Name = %30s, Prefix = %s => %s, Address = %s => %s, Active = %s => %s" % (req_user, req_pref, new_pref, req_addr, new_addr, req_text, new_text))
								else:
									print("\t\t\t\t  Route Request: Name = %30s, Prefix = %s, Address = %s, Active = %s" % (req_user, req_pref, req_addr, req_text))
								pass
							pass
						pass
					pass
				pass
			pass
		pass
	pass
	#
	# Traverse the XML tree and update the node elements
	#
	def Update(self, cb_get_discipline, cb_get_block, cb_get_signal, cb_get_turnout):

		new_discipline = cb_get_discipline()
		
		for child in self.mXmlRoot:
			if (child.tag == "TRACKPLAN"):
				self.mNumCols = int(child.get('COLUMNS').replace("\n", ""))
				self.mNumRows = int(child.get('ROWS').replace("\n", ""))
				for section in child.iter('SECTION'):
					section_x = int(section.get('X').replace("\n", ""))
					section_y = int(section.get('Y').replace("\n", ""))
					new_x = section_x + self.mXOffset
					new_y = section_y + self.mYOffset
#					section.set('X', "%d" % (new_x))
#					section.set('X', "%d" % (new_y))
				pass

				for block in child.iter('BLOCK'):
					if (block.get('NAME') != None):
						block_name = block.get('NAME').replace("\n", "")
						block_disc = block.get('DISCIPLINE').replace("\n","")
						if block_disc != "ABS":
							block_disc = block.set('DISCIPLINE', "%s" % new_discipline)
						for occupy in block.iter('OCCUPIEDSPEC'):
							for iospec in occupy.iter('IOSPEC'):
								block_user = iospec.get('USER_NAME').replace("\n", "")
								new_pin    = cb_get_block(block_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									iospec.set('JMRIPREFIX', "%s" % new_pref)
									iospec.set('DECADDR', "%s" % new_addr)
									iospec.text = "%s" % new_text
								pass
							pass
						pass
						for unoccupy in block.iter('UNOCCUPIEDSPEC'):
							for iospec in unoccupy.iter('IOSPEC'):
								block_user = iospec.get('USER_NAME').replace("\n", "")
								new_pin    = cb_get_block(block_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									if (new_text == "throw"):
										new_text = "close"
									pass
									iospec.set('JMRIPREFIX', "%s" % new_pref)
									iospec.set('DECADDR', "%s" % new_addr)
									iospec.text = "%s" % new_text
								pass
							pass
						pass
					pass
				pass
				for head in child.iter('SECSIGNAL'):
					head_name = head.text
					head_name = head_name.replace("\n", "")
					head_name = head_name.lstrip()
					for aspect in head.iter('ASPECTCOMMAND'):
						head_color = aspect.get('PLABEL').replace("\n", "")
						for iospec in aspect.iter('IOSPEC'):
							head_user = iospec.get('USER_NAME').replace("\n", "")
							new_pin = cb_get_signal(head_user)
							if (len(new_pin) == 3):
								new_pref = new_pin[0]
								new_addr = new_pin[1]
								new_text = new_pin[2]
								iospec.set('JMRIPREFIX', "%s" % new_pref)
								iospec.set('DECADDR', "%s" % new_addr)
								iospec.text = "%s" % new_text
							pass
						pass
					pass
				pass
				for switchpoint in child.iter('SWITCHPOINTS'):
					for points in switchpoint.iter('POINTSMSG'):
						for iospec in points.iter('IOSPEC'):
							pnt_pref = iospec.get('JMRIPREFIX').replace("\n", "")
							pnt_addr = iospec.get('DECADDR').replace("\n", "")
							pnt_user = iospec.get('USER_NAME').replace("\n", "")
							pnt_text = iospec.text
							new_pin  = cb_get_turnout(pnt_user)
							if (len(new_pin) == 3):
								new_pref = new_pin[0]
								new_addr = new_pin[1]
								new_text = new_pin[2]
								iospec.set('JMRIPREFIX', "%s" % new_pref)
								iospec.set('DECADDR', "%s" % new_addr)
								iospec.text = "%s" % new_text
							pass
						pass
					pass
					for route in switchpoint.iter('ROUTEINFO'):
						route_id = route.get('ROUTEID').replace("\n", "")
						route_norm = route.get('NORMAL')
						if (route_norm == "true"):
							normal = True
						else:
							normal = False
						pass	
						for report in route.iter('SELECTEDREPORT'):
							for iospec in report.iter('IOSPEC'):
								rpt_user = iospec.get('USER_NAME').replace("\n", "")
								new_pin	 = cb_get_turnout(rpt_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									iospec.set('JMRIPREFIX', "%s" % new_pref)
									iospec.set('DECADDR', "%s" % new_addr)
									if (normal):
										iospec.text = "%s" % new_text
									else:
										if (new_text == "throw"):
											new_text = "close"
										else:
											new_text = "throw"
										pass
									pass
									iospec.text = "%s" % new_text
								pass
							pass
						pass
						for report in route.iter('NOTSELECTEDREPORT'):
							for iospec in report.iter('IOSPEC'):
								rpt_user = iospec.get('USER_NAME').replace("\n", "")
								new_pin	 = cb_get_turnout(rpt_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									iospec.set('JMRIPREFIX', "%s" % new_pref)
									iospec.set('DECADDR', "%s" % new_addr)
									if (not normal):
										iospec.text = "%s" % new_text
									else:
										if (new_text == "throw"):
											new_text = "close"
										else:
											new_text = "throw"
										pass
									pass
									iospec.text = "%s" % new_text
								pass
							pass
						pass
						for command in route.iter('ROUTECOMMAND'):
							for iospec in command.iter('IOSPEC'):
								cmd_user = iospec.get('USER_NAME').replace("\n", "")
								new_pin  = cb_get_turnout(cmd_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									iospec.set('JMRIPREFIX', "%s" % new_pref)
									iospec.set('DECADDR', "%s" % new_addr)
									if (normal):
										iospec.text = "%s" % new_text
									else:
										if (new_text == "throw"):
											new_text = "close"
										else:
											new_text = "throw"
										pass
									pass
									iospec.text = "%s" % new_text
								pass
							pass
						pass
						for request in route.iter('ROUTEREQUEST'):
							for iospec in request.iter('IOSPEC'):
								req_pref = iospec.get('JMRIPREFIX').replace("\n", "")
								req_addr = iospec.get('DECADDR').replace("\n", "")
								req_user = iospec.get('USER_NAME').replace("\n", "")
								req_text = iospec.text
								new_pin  = cb_get_turnout(req_user)
								if (len(new_pin) == 3):
									new_pref = new_pin[0]
									new_addr = new_pin[1]
									new_text = new_pin[2]
									iospec.set('JMRIPREFIX', "%s" % new_pref)
									iospec.set('DECADDR', "%s" % new_addr)
									if (normal):
										iospec.text = "%s" % new_text
									else:
										if (new_text == "throw"):
											new_text = "close"
										else:
											new_text = "throw"
										pass
									pass
									iospec.text = "%s" % new_text
								pass
							pass
						pass
					pass
				pass
			pass
		pass
	pass
pass
