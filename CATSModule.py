import sys
import pyexcel
import pyexcel_xlsx
from CATSxml import CATSxml

##################################################################################################################
#
# Excel Module Functions
#
##################################################################################################################
#
# Pin Class
#
# This class represents one hardware pin on a module. A pin can be either an input or an output and may be used
# with Block Detectors, Signal Heads, or Turnouts
#
# mName:		Pin Name
# mDir:			Pin Direction (IN or OUT)
# mPrefix:		JMRI Device Pin Prefix
# mAddress:		JMRI Device Pin Address
# mPinIsDCC:	True if the mAddress is DCC
# mActiveState:	JMRI Active State (Throw or Close)
#
##################################################################################################################
class Pin:
	#
	# Constructor
	#
	def __init__(self, pin_name, pin_dir, pin_prefix, pin_address, pin_is_dcc, pin_active):
		self.mName = pin_name
		self.mDir = pin_dir
		self.mPrefix = pin_prefix
		self.mAddress = pin_address
		self.mPinIsDCC = pin_is_dcc
		self.mActiveState = pin_active
	pass
	#
	# Returns mName
	#
	def get_name(self):
		return self.mName
	pass
	#
	# Returns mDir
	#
	def get_dir(self):
		return self.mDir
	pass
	#
	# Returns mPrefix
	#
	def get_prefix(self):
		return self.mPrefix
	pass
	#
	# Returns mAddress
	#
	def get_address(self):
		return self.mAddress
	pass
	#
	# Returns true if mAddress is DCC
	#
	def get_is_dcc(self):
		return self.mPinIsDCC
	pass
	#
	# Returns mActiveState
	#
	def get_active(self):
		return self.mActiveState
	pass
	#
	# Returns the CATS name from the given prefix
	#
	def get_cats_name(self, cats_prefix):
		return "%s:%s" % (cats_prefix, self.mName)
	pass
	#
	# Print out the pin information
	#
	def print_pin(self, node_name):
		print("\tDIR = %3s, Name = %-20s, Prefix = %s, Address = %6s, Active = %s, CATS Object: %s" % (self.mDir, self.mName, self.mPrefix, self.mAddress, self.mActiveState, self.get_cats_name(node_name)))
	pass
pass
##################################################################################################################
#
# Node Class
#
# This class represents a single module node that's on the layout signaling network
#
# mNodeID:					Name of the node worksheet tab in the Excel workbook this information came from
# mControlNodeName:			This is the JMRI control node name used to make each pin unique in the system
# mNewDiscipline:			New CATS discipline
# mBaseControlNode:			Configuration name of the base node of this node on the layout signaling network
# mIOXControlNodes:			List of IO Expanders attached to the base node
# mNewDCCNodePrefix:		JMRI prefex of the new DCC node to use in this system
# mNewControlNodePrefix:	JMRI prefex of the new control node to use in this system
# mBlockPins:				List of pins used for block detectors
# mSignalPins:				List of pins used for signal heads
# mTurnoutPins:				List of pins used for turnouts
# mNodeXML:					XML tree of the CATS information for this node
# 
##################################################################################################################
class Node:
	#
	# Constructor
	#
	def __init__(self, nodeid):
		self.mNodeID = nodeid
		self.mControlNodeName = ""
		self.mNewDiscipline = ""
		self.mBaseControlNode = ""
		self.mIOXControlNodes = []
		self.mNewDCCNodePrefix = ""
		self.mNewControlNodePrefix = ""
		self.mBlockPins = []
		self.mSignalPins = []
		self.mTurnoutPins = []
		self.mNodeXML = None
	pass
	#
	# Set the mControlNodeName
	#
	def set_control_node_name(self, prefix):
		self.mControlNodeName = prefix
	pass
	#
	# Set the new mDCCNodePrefix
	#
	def set_new_dcc_node_prefix(self, prefix):
		self.mNewDCCNodePrefix = prefix
	pass
	#
	# Set the new mControlNodePrefix
	#
	def set_new_control_node_prefix(self, prefix):
		self.mNewControlNodePrefix = prefix
	pass
	#
	# Set the new discipline
	#
	def set_new_discipline(self, discipline):
		self.mNewDiscipline = discipline
	pass
	#
	# Get the new mNewDCCNodePrefix
	#
	def get_new_dcc_node_prefix(self):
		return self.mNewDCCNodePrefix
	pass
	#
	# Get the new mNewNodePrefix
	#
	def get_new_node_prefix(self):
		return self.mNewNodePrefix
	pass
	#
	# Return this node's mNewDiscipline
	#
	def get_new_discipline(self):
		return self.mNewDiscipline
	pass
	#
	# Returns the number of pins for blocks
	#
	def get_num_blocks(self):
		return len(self.mBlockPins)
	pass
	#
	# Returns the number of pins for signals
	#
	def get_num_signals(self):
		return len(self.mSignalPins)
	pass
	#
	# Returns the number of pins for turnouts
	#
	def get_num_turnouts(self):
		return len(self.mTurnoutPins)
	pass
	#
	# Return this node's mControlNodeName
	#
	def get_control_node_name(self):
		return self.mControlNodeName
	pass
	#
	# Print the contects of this node
	#
	def print_node(self):
		print("Node Information Found in the Excel Configuration Worksheet(s)")
		print("Node ID '%s' is Control Node '%s'" % (self.mNodeID, self.mControlNodeName))
		self.print_base_control_node()
		self.print_iox_control_nodes()
		self.print_pins()
	pass
	#
	# Set the mBaseNode name
	#
	def set_base_control_node(self, base):
		self.mBaseControlNode = base
	pass
	#
	# Add the name of the given IO expander to the list of IO expanders
	#
	def add_iox_control_node(self, iox):
		self.mIOXControlNodes.append(iox)
	pass
	#
	# Print the base node name
	#
	def print_base_control_node(self):
		print("Base Control Node: %s" % self.mBaseControlNode)
	pass
	#
	# Print the IO expander node names
	#
	def print_iox_control_nodes(self):
		for iox in self.mIOXControlNodes:
			print(" IOX Control Node: %s" % iox)
		pass
	pass
	#
	# Add the given pin to the corresponding list
	#
	def add_pin(self, pin_type, pin_name, pin_dir, pin_prefix, pin_address, pin_is_dcc, pin_active):
		new_pin = Pin(pin_name, pin_dir, pin_prefix, pin_address, pin_is_dcc, pin_active)
		if (pin_type == 'BLOCK'):
			self.mBlockPins.append(new_pin)
		elif (pin_type == 'SIGNAL'):	
			self.mSignalPins.append(new_pin)
		elif (pin_type == 'TURNOUT'):	
			self.mTurnoutPins.append(new_pin)
		else:
			print("Unknown pin type: %s" % pin_type)
		pass
	pass
	#
	# Print all the pins associated with this node
	#
	def print_pins(self):
		if (self.get_num_blocks() > 0):
			print("Node Block Pins:")
			for pin in self.mBlockPins:
				pin.print_pin(self.mControlNodeName)
			pass
		pass
		if (self.get_num_signals() > 0):
			print("Node Signal Pins:")
			for pin in self.mSignalPins:
				pin.print_pin(self.mControlNodeName)
			pass
		pass
		if (self.get_num_turnouts() > 0):
			print("Node Turnout Pins:")
			for pin in self.mTurnoutPins:
				pin.print_pin(self.mControlNodeName)
			pass
		pass
	pass
	#
	# Check for a CATS block node
	#
	def has_cats_block_pin(self, cats_name):
		retval = False
		cats_prefix = self.mControlNodeName
		for block_pin in self.mBlockPins:
			cats_pin_name = block_pin.get_cats_name(cats_prefix)
#			print("Block: %s %s" % (cats_name, cats_pin_name))
			if (cats_pin_name in cats_name):
				retval = True
				break
			pass
		pass
		return retval
	pass
	#
	# Check for a CATS signal node
	#
	def has_cats_signal_pin(self, cats_name):
		retval = False
		cats_prefix = self.mControlNodeName
		for signal_pin in self.mSignalPins:
			cats_pin_name = signal_pin.get_cats_name(cats_prefix)
#			print("Signal: %s %s" % (cats_name, cats_pin_name))
			if (cats_pin_name in cats_name):
				retval = True
				break
			pass
		pass
		return retval
	pass
	#
	# Check for a CATS turnout node
	#
	def has_cats_turnout_pin(self, cats_name):
		retval = False
		cats_prefix = self.mControlNodeName
		for turnout_pin in self.mTurnoutPins:
			cats_pin_name = turnout_pin.get_cats_name(cats_prefix)
#			print("Turnout: %s %s" % (cats_name, cats_pin_name))
			if (cats_pin_name in cats_name):
				retval = True
				break
			pass
		pass
		return retval
	pass
	#
	# Return the pins for the given block if it was found in the spreadsheet
	#
	def get_cats_block_pin(self, cats_name):
		retval = []
		cats_prefix = self.mControlNodeName
		for pin in self.mBlockPins:
			cats_pin_name = pin.get_cats_name(cats_prefix)
			if (cats_pin_name in cats_name):
				pin_prefix = pin.get_prefix()
				new_prefix = "%s%s" % (self.mNewControlNodePrefix, pin_prefix[1])	# create the new prefix
				pin_addr = pin.get_address()
				pin_is_dcc = pin.get_is_dcc()
				pin_text = pin.get_active()
				pin_text = pin_text.lower()
				retval = [new_prefix, pin_addr, pin_text]
				break
			pass
		pass
		return retval
	pass
	#
	# Return the pins for the given signal if it was found in the spreadsheet
	#
	def get_cats_signal_pin(self, cats_name):
		retval = []
		cats_prefix = self.mControlNodeName
		for pin in self.mSignalPins:
			cats_pin_name = pin.get_cats_name(cats_prefix)
			if (cats_pin_name in cats_name):
				pin_prefix = pin.get_prefix()
				new_prefix = "%s%s" % (self.mNewControlNodePrefix, pin_prefix[1])	# create the new prefix
				pin_addr = pin.get_address()
				pin_is_dcc = pin.get_is_dcc()
				pin_text = pin.get_active()
				pin_text = pin_text.lower()
				retval = [new_prefix, pin_addr, pin_text]
				break
			pass
		pass
		return retval
	pass
	#
	# Return the pins for the given turnout if it was found in the spreadsheet
	#
	def get_cats_turnout_pin(self, cats_name):
		retval = []
		cats_prefix = self.mControlNodeName
		for pin in self.mTurnoutPins:
			cats_pin_name = pin.get_cats_name(cats_prefix)
			if (cats_pin_name in cats_name):
				pin_prefix = pin.get_prefix()
				pin_addr = pin.get_address()
				pin_is_dcc = pin.get_is_dcc()
				if (pin_is_dcc):
					new_prefix = "%s%s" % (self.mNewDCCNodePrefix, pin_prefix[1])  # use the DCC node prefix
				else:
					new_prefix = "%s%s" % (self.mNewControlNodePrefix, pin_prefix[1])	# use the control node prefix
				pass
				pin_text = pin.get_active()
				pin_text = pin_text.lower()
				retval = [new_prefix, pin_addr, pin_text]
				break
			pass
		pass
		return retval
	pass
	#
	# Get the node's CATS XML
	#
	def add_xml(self, name):
		self.mNodeXML = CATSxml(name)
		self.mNodeXML.Read()
	pass
	#
	# Print out this node's xml
	#
	def dump_xml(self):
		self.mNodeXML.Print(self.get_new_discipline, self.get_cats_block_pin, self.get_cats_signal_pin, self.get_cats_turnout_pin)
	pass
	#
	# Print out this node's debug xml
	#
	def debug_dump_xml(self):
		self.mNodeXML.DebugDump()
	pass
	#
	# Update the XML
	#
	def update_xml(self):
		self.mNodeXML.Update(self.get_new_discipline, self.get_cats_block_pin, self.get_cats_signal_pin, self.get_cats_turnout_pin)
	pass
	#
	# Write out the CATS XML
	#
	def write_xml(self):
		self.mNodeXML.Write()
	pass
pass
##################################################################################################################
#
# Main Module Class
#
# This class contains all of the information associated with a module
#
# mDefaultDCCNodePrefix:	Sets the default JMRI Device Prefix for the DCC Command Stations used with this module
# mNewDCCNodePrefix:		Sets the new JMRI Device Prefix for the DCC Command Stations used with this module
# mNewControlNodePrefix:	Sets the new JMRI control node prefix
# mNewDiscipline:			Sets the new JMRI Discipline for this moodule (CTC, APB, etc)
# mNodeWB:					Name of the Excel Workbook that contained this information
# mNodeSheets:				A list of the names of all the sheets used to define the nodes on this module
# mNodes:					A list of all nodes installed in this module
#
##################################################################################################################
class CATSModule:
	#
	# Constructor
	#
	def __init__(self):
		self.mDefaultDCCNodePrefix = ""
		self.mNewDCCNodePrefix = ""
		self.mNewControlNodePrefix = ""
		self.mNewDiscipline = ""
		self.mNodeWB = None
		self.mNodes = []
		self.mNodeSheets = []
	pass
	#
	# Sets the default JMRI DCC prefix
	#
	def set_default_dcc_node_prefix(self, prefix):
		self.mDefaultDCCNodePrefix = prefix
	pass
	#
	# Sets the new JMRI DCC prefix
	#
	def set_new_dcc_node_prefix(self, prefix):
		self.mNewDCCNodePrefix = prefix
	pass
	#
	# Sets the new JMRI Node prefix
	#
	def set_new_control_node_prefix(self, prefix):
		self.mNewControlNodePrefix = prefix
	pass
	#
	# Sets the new CATS Discipline
	#
	def set_new_discipline(self, discipline):
		self.mNewDiscipline = discipline
	pass
	#
	# Gets the default JMRI DCC prefix
	#
	def get_default_dcc_node_prefix(self):
		return self.mDefaultDCCNodePrefix
	pass
	#
	# Gets the new JMRI DCC prefix
	#
	def get_new_dcc_node_prefix(self):
		return self.mNewDCCNodePrefix
	pass
	#
	# Gets the new JMRI Node prefix
	#
	def get_new_node_prefix(self):
		return self.mNewNodePrefix
	pass
	#
	# Gets the new CATS Discipline
	#
	def get_new_discipline(self):
		return self.mNewDiscipline
	pass
	#
	# Add a new node to the module
	#
	def add_node(self, newNode):
		self.mNodes.append(newNode)
	pass
	#
	# Returns the list of worksheets that defined this module
	#
	def get_node_sheets(self):
		return self.mNodeSheets
	pass
	#
	# Returns the list of node names
	#
	def get_node_prefixes(self):
		plist = []
		for node in self.mNodes:
			plist.append(node.get_node_prefix())
		pass
		return plist
	pass
	#
	# Prints all of the node information for this module
	#
	def print_nodes(self):
		for thisNode in self.mNodes:
			thisNode.print_node()
		pass
	pass
	#
	# Opens the given workbook file and returs the number of configuration worksheets found
	#
	def open_workbook(self, filename):
		print("Node definition File: %s" % filename)
		try:
			self.mNodeWB = pyexcel.get_book(file_name=filename)
		except:
			print("Spreadsheet Error: ", sys.exc_info()[0])
			raise
		pass
	
		for sheet in self.mNodeWB.to_dict().keys():
			sheet_title = self.mNodeWB[sheet][0,0]
			if ("Configuration Worksheet" in sheet_title):
				self.mNodeSheets.append(sheet)
			pass
		pass
	
		if len(self.mNodeSheets) == 0:
			print("No Configureation Worksheets Found!")
		pass
	
		self.process_worksheets()
		
		return len(self.mNodeSheets)
	pass
	#
	# Process the worksheets found and create the nodes
	#
	def process_worksheets(self):
		if (len(self.mNodeSheets) == 0):
			print("No Node Worksheets Found!")
			return
		pass

		for nodesheet in self.mNodeSheets:
			newNode = Node(nodesheet)
			newNode.set_new_dcc_node_prefix(self.mNewDCCNodePrefix)
			newNode.set_new_control_node_prefix(self.mNewControlNodePrefix)
			newNode.set_new_discipline(self.mNewDiscipline)
		
			base_row = 4
			base_col = 2
		
			node_base = self.mNodeWB[nodesheet][base_row, base_col]
			newNode.set_base_control_node(node_base)
		
			start_row = 16 - 1
			if (node_base == 'SMINI'):
				last_row = 87 - 1
			else:
				last_row = 159 - 1
				for iox_row in range(base_row+1, base_row+9):
					node_iox = self.mNodeWB[nodesheet][iox_row, base_col]
					if (node_iox != '-'):
						newNode.add_iox_control_node(node_iox)
					pass
				pass
			pass

			dir_col = 0	
			name_col = 1
			type_col = 2
			id_col = 14
			dcc_col  = 4
			state_col = 5
			jmri_col = 11

			node_name = self.mNodeWB[nodesheet][start_row, name_col]
			newNode.set_control_node_name(node_name)

			done = False
			cur_row = start_row
			while (not done):
				pin_dir    = self.mNodeWB[nodesheet][cur_row, dir_col]
				pin_type   = self.mNodeWB[nodesheet][cur_row, type_col]
				pin_id     = self.mNodeWB[nodesheet][cur_row, id_col]
				pin_jmri   = self.mNodeWB[nodesheet][cur_row, jmri_col]
				pin_prefix = pin_jmri[0:2]	# just the first two characters are the device prefix
				pin_addr   = pin_jmri[2:]	# everything else is the address
				pin_dcc    = self.mNodeWB[nodesheet][cur_row, dcc_col]
				pin_state  = self.mNodeWB[nodesheet][cur_row, state_col]
				pin_is_dcc = False
				if (pin_dcc != '-'):
					if (pin_dir == 'IN'):
						pin_prefix = "%sS" % self.mDefaultDCCNodePrefix
					else:
						pin_prefix = "%sT" % self.mDefaultDCCNodePrefix
					pass
					pin_is_dcc = True
					pin_addr = pin_dcc
				pass
				object_type = 'unassigned'
				if (pin_type != 'Unassigned'):
					if ((pin_type == 'Occupied Report') or (pin_type == 'Unoccupied Report')):
						object_type = 'BLOCK'
					elif (pin_type == 'Signal Head'):
						object_type = 'SIGNAL'
					elif ((pin_type == 'Route Selected Report') or (pin_type == 'Route Unselected Report') or (pin_type == 'Select Route Command') or (pin_type == 'Select Route Request') or (pin_type == 'Turnout Locked Report') or (pin_type == 'Turnout Unlocked Report') or (pin_type == 'Turnout Locked Light On') or (pin_type == 'Turnout Unlocked Light On')):
						 object_type = 'TURNOUT'
					pass
				if (object_type != 'unassigned'):
					newNode.add_pin(object_type, pin_id, pin_dir, pin_prefix, pin_addr, pin_is_dcc, pin_state)
				pass
				if (cur_row == last_row):
					done = True
				else:
					cur_row = cur_row + 1
				pass
			pass
		
			newNode.add_xml(node_name)
			self.add_node(newNode)
		pass	
	pass
	#
	# Print out all node information
	#
	def print_nodes(self):
		for node in self.mNodes:
			print("\n==========================================================================================================================================")
#			node.print_node()
#			print("------------------------------------------------------------------------------------------------------------------------------------------")
###			node.dump_xml()
			node.update_xml()
			node.write_xml()
#			node.debug_dump_xml()	
		pass
		print("==========================================================================================================================================")
	pass
pass

