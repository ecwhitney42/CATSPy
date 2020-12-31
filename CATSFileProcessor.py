#!/usr/bin/env python3

import sys
from CATSModule import CATSModule

##################################################################################################################
#
# Main
#
##################################################################################################################

if (len(sys.argv) < 2):
	print("\nUsage: %s <module_node_spreadsheet>\n" % (sys.argv[0]))
	sys.exit(-1)

workbook_filename = sys.argv[1]
default_dcc_node_prefix	= "N"
new_dcc_node_prefix		= "X"
new_control_node_prefix	= "C"
new_discipline			= "CTC"
	
module = CATSModule()
module.set_default_dcc_node_prefix(default_dcc_node_prefix)
module.set_new_dcc_node_prefix(new_dcc_node_prefix)
module.set_new_control_node_prefix(new_control_node_prefix)
module.set_new_discipline(new_discipline)

nodes_found = module.open_workbook(workbook_filename)

module.print_nodes()

sys.exit(0)


