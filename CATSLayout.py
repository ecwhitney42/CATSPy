import sys
import os
import pyexcel
import pyexcel_xlsx
import xml.etree.ElementTree as ET

##################################################################################################################
#
# XML Examples
#
##################################################################################################################
#
# XML needed for the last section to loop back to the first:
#
# Transform from:
#
#<SECTION X="126" Y="3">
#  <TRACKGROUP>
#	<TRACK>HORIZONTAL</TRACK>
#  </TRACKGROUP>
#  <SEC_EDGE EDGE="RIGHT" />
#  <SEC_EDGE EDGE="LEFT" />
#</SECTION>
#
# To:
#
#<SECTION X="126" Y="3">
#  <TRACKGROUP>
#	<TRACK>HORIZONTAL</TRACK>
#  </TRACKGROUP>
#  <SEC_EDGE EDGE="RIGHT">
#	<SHARED X="1" Y="3">LEFT</SHARED>
#  </SEC_EDGE>
#  <SEC_EDGE EDGE="LEFT" />
#</SECTION>
#
##################################################################################################################
#
# XML Functions
#
##################################################################################################################
class CATSModuleXML:
	def __init__(self, name):
		self.mModuleName = name
		self.mFileName = "%s.xml" % name
		self.mXmlTree = None
		self.mXmlRoot = None
		self.mXOffset = 0
		self.mYOffset = 0
		self.mNumRows = 0
		self.mNumCols = 0
	pass

	def get_name(self):
		return(self.mModuleName)
	pass

	def get_size(self):
		return([self.mNumRows, self.mNumCols])
	pass

	def get_tree(self):
		return(self.mXmlTree)
	pass

	def get_root(self):
		return(self.mXmlRoot)
	pass

	def set_size(self, rows, cols):
		self.mNumRows = rows
		self.mNumCols = cols
	pass

	def set_xml(self, xml_tree, rows, cols):
		self.mXmlTree = xml_tree
		self.mXmlRoot = xml_tree.getroot()
		self.mNumRows = rows
		self.mNumCols = cols
		return
	pass

	def read_xml(self):
		print("Reading XML %s..." % self.mFileName)
		try:
			self.mXmlTree = ET.parse(self.mFileName)
			self.mXmlRoot = self.mXmlTree.getroot()
		except:
			print("XML File Error: ", sys.exc_info()[0])
			raise
		pass
		#
		# Read the size of the module
		#
		for child in self.mXmlRoot:
			if (child.tag == "TRACKPLAN"):
				self.mNumCols = int(child.get('COLUMNS').replace("\n", ""))
				self.mNumRows = int(child.get('ROWS').replace("\n", ""))
				print("\tXML Track Plan %s is (%d wide x %d high)" % (self.mModuleName, self.mNumCols, self.mNumRows))
				break
			pass
		pass
		return
	pass

	def write_xml(self):
		print("Writing XML File: %s..." % self.mFileName)
		self.mXmlTree.write(self.mFileName)
	pass
pass	
 
##################################################################################################################
#
# Main Module Class
#
# This class contains all of the information associated with a layout
#
#
##################################################################################################################
class CATSLayout:
	#
	# Constructor
	#
	def __init__(self):
		self.mLayoutName = ""
		self.mLayoutWB = None
		self.mLayoutWS = None
		self.mTransformWS = None
		self.mLayoutRows = 0
		self.mLayoutCols = 0
		self.mModules = []
		self.mLayout = None
		self.mLeftSectionEdges = []
		self.mTransforms = []
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
	# Add a new module to the layout
	#
	def add_node(self, newModule):
		self.mModules.append(newModule)
	pass
	#
	# Returns the list of worksheets that defined this module
	#
	def get_node_sheets(self):
		return self.mNodeSheets
	pass
	#
	# Prints all of the node information for this module
	#
	def print_modules(self):
		for thisModule in self.mModules:
			thisModule.print()
		pass
	pass
	#
	# Opens the given workbook file and returs the number of configuration worksheets found
	#
	def open_workbook(self, filename):
		#
		# Read the spreadsheet
		#
		print("Layout definition File: %s" % filename)
		try:
			self.mLayoutWB = pyexcel.get_book(file_name=filename)
			self.mLayoutWS = self.mLayoutWB['Modules']
			self.mTransformWS = self.mLayoutWB['Transforms']
		except:
			print("Spreadsheet Error: ", sys.exc_info()[0])
			raise
		pass
		#
		# Create the layout XML filename
		#
		name = os.path.basename(filename)
		base = os.path.splitext(name)
		self.mLayoutName = base[0]
		#
		# Read in the module filenames
		#
		first = True
		for row in self.mLayoutWS.rows():
			if (first):
				first = False
				continue
			pass
			name = row[0]
			#
			# Create a module for each XML file
			#
			module = CATSModuleXML(name)
			module.read_xml()
			#
			# Get the size of the module
			#
			[num_rows, num_cols] = module.get_size()
			#
			# This sets the number of rows to the max rows found
			#
			if (num_rows > self.mLayoutRows):
				self.mLayoutRows = num_rows
			pass
			#
			# Accumulate the number of columns--we build the layout as a single row
			#
			self.mLayoutCols = self.mLayoutCols + num_cols
			#
			# Finally add this module to the layout list
			#
			self.mModules.append(module)
		pass
		#
		# Process the transforms
		#
		first = True
		for row in self.mTransformWS.rows():
			if (first):
				first = False
				continue
			pass
			transform = (row[0], row[1], row[2], row[3])
			self.mTransforms.append(transform)
		pass
		print("%d Transforms Found" % len(self.mTransforms))
		#
		# Return the number of modules found
		#
		return len(self.mModules)
	pass
	#
	# Print out all node information
	#
	def print_modules(self):
		print("\nLayout: %s (Final Size will be: %dh x %dw)" % (self.mLayoutName, self.mLayoutRows, self.mLayoutCols))
		print("==========================================================================================================================================")
		for module in self.mModules:
			[rows, cols] = module.get_size()
			print("Module: %s (%dh x %dw)" % (module.get_name(), rows, cols))
		pass
		print("==========================================================================================================================================")
	pass
	#
	# Create the layout
	#
	def create_layout(self):
		#
		# copy the first module into the layout as a satrting point
		#
		self.mLayout = CATSModuleXML(self.mLayoutName)
		self.mLayout.set_xml(self.mModules[0].get_tree(), self.mLayoutRows, self.mLayoutCols)
		#
		# Find the section edges on the left side of the first module
		#
		for layout_child in self.mLayout.mXmlRoot:
			for section in layout_child.iter('SECTION'):
				x_value = int(section.get('X').replace("\n",""))
				y_value = int(section.get('Y').replace("\n",""))
				if (x_value == 1):
					self.mLeftSectionEdges.append(y_value)
				pass
			pass
		pass
		print("The layout has %d track edges on the left side" % len(self.mLeftSectionEdges))
		#
		# go to the trackplan
		#
		col_offset = 0
		for layout_child in self.mLayout.mXmlRoot:
			#
			# Only edit elements under the TRACKPLAN
			#
			if (layout_child.tag == 'TRACKPLAN'):
				#
				# Update the layout size with the final number of columns and rows
				#
				layout_child.set('COLUMNS', "%d" % self.mLayoutCols)
				layout_child.set('ROWS', "%d" % self.mLayoutRows)
				#
				# Iteration through each module and copy over each SECTION
				#
				for module_index in range(1, len(self.mModules)):
					#
					# Calculate the X-offset as we add each module to the right
					#
					prev_module_size = self.mModules[module_index-1].get_size()
					col_offset = col_offset + prev_module_size[1]
					#
					# Get the root of the module
					#
					this_module = self.mModules[module_index].get_root()
					#
					# Iterate through the children
					#
					for module_child in this_module:
						#
						# Find TRACKPLAN first
						#
						if (module_child.tag == 'TRACKPLAN'):
							#
							# Now go through the sections
							#
							for module_section in module_child.iter('SECTION'):
								#
								# Update each section with the correct X offset
								#
								section_x = int(module_section.get('X').replace("\n","")) + col_offset
								section_y = int(module_section.get('Y').replace("\n",""))
								module_section.set('X', "%d" % section_x)
								#
								# Check if this section is on the right edge of the layout
								# and that the left edge has a section at the same y location
								#
								if ((section_x == self.mLayoutCols) and (section_y in self.mLeftSectionEdges)):
									print("Found right track edge at (%d, %d), connecting to (%d, %d)" % (section_x, section_y, 1, section_y))
									#
									# We only need to edit the RIGHT SEC_EDGE
									#
									for module_secedge in module_section.iter('SEC_EDGE'):
										edge = module_secedge.get('EDGE').replace("\n","")
										if (edge == "RIGHT"):
											#
											# Create the new SHARED element needed
											#
											shared = ET.Element('SHARED')
											shared.set('X', '1')
											shared.set('Y', "%d" % section_y)	
											shared.text = 'LEFT'	# this is the left edge of section 1,3
											module_secedge.append(shared)
											pass
										pass
									pass
								pass
								#
								# now add the section to the layout
								#
								layout_child.append(module_section)
							pass
						pass
					pass
				pass
			pass
		pass
	pass
	#
	# Update objects in the XML
	#
	# Search for 'object', then check if 'item' has 'old_value', if so, replace with 'new_value'
	#
	def edit_object(self, object, item, old_value, new_value):
		print("Transorm object %s, item %s, %s => %s" % (object, item, old_value, new_value))
		for child in self.mLayout.mXmlRoot:
			for obj in child.iter(object):
				current_value = obj.get(item)
				if (current_value == old_value):
					obj.set(item, "%s" % new_value)
				pass
			pass
		pass
	pass
	#
	# Process the transforms found
	#
	def process_transforms(self):
		for transform in self.mTransforms:
			self.edit_object(transform[0], transform[1], transform[2], transform[3])
		pass
		print("Processed %d transformations" % len(self.mTransforms))
	pass
	#
	# Save the layout file
	#
	def save_layout(self):
		self.mLayout.write_xml()
	pass
pass

