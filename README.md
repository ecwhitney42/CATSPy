# CATSPy
 Python Library for processing CATS XML files

## Introduction

The goal of this project is to provide a set of utilities for managing CATS XML files for configuring modular layouts. 

**CATSFileProcessor.py**

The CATSFileProcessor utility is designed to take a set of CATS module layout template files and update them with IO port information contained in a spreadsheet.

```bash
CATSFileProcessor.py module_node_definition_spreadsheet.xlsx
```

**CATSLayoutGenerator.py**

The CATSLayoutGenerator utility takes a spreadsheet description of a layout and assembles the aforementioned CATS XML files into a single layout file. There are two parts to the layout description spreadsheet. On sheet, called 'Modules', contains a list of the names of each CATS XML file. The second shee, called 'Transforms', contains a list of items in the XML that need to be updated for the layout to work properly (i.e. setting DISCIPLINE to 'CTC' or 'APB-2') or setting the proper JMRIPREFIX for any DCC decoders so that they work with the layout's DCC system.

```bash
CATSLayoutGenerator.py layout_definition_spreadsheet.xlsx
```
## Details

More detailed documentation is in process...
