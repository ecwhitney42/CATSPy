#!/usr/bin/env python3

import sys
from CATSLayout import CATSLayout

##################################################################################################################
#
# Main
#
##################################################################################################################

if (len(sys.argv) < 2):
	print("\nUsage: %s <layout_definition_spreadsheet>\n" % (sys.argv[0]))
	sys.exit(-1)

workbook_filename = sys.argv[1]
	
layout = CATSLayout()

modules_found = layout.open_workbook(workbook_filename)

layout.print_modules()

layout.create_layout()

layout.process_transforms()

#layout.edit_object('BLOCK', 'DISCIPLINE', 'CTC', 'APB-2')
#layout.edit_object('BLOCK', 'DISCIPLINE', 'ABS', 'APB-2')

#layout.edit_object('IOSPEC', 'JMRIPREFIX', 'NT', 'XT')
#layout.edit_object('IOSPEC', 'JMRIPREFIX', 'NS', 'XS')

layout.save_layout()

sys.exit(0)


