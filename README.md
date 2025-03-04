# CATSPy
 Python Library for processing CATS XML files

## Introduction

The goal of this project is to provide a set of utilities for managing CATS XML files for configuring modular layouts. 

**CATSFileProcessor.py**

The CATSFileProcessor utility is designed to take a set of CATS module layout template files and update them with IO port information contained in a spreadsheet.

```bash
cd Examples
../CATSFileProcessor.sh ExampleModuleDefinitions.xlsx
```

**CATSLayoutGenerator.py**

The CATSLayoutGenerator utility takes a spreadsheet description of a layout and assembles the aforementioned CATS XML files into a single layout file. There are two parts to the layout description spreadsheet. On sheet, called 'Modules', contains a list of the names of each CATS XML file. The second shee, called 'Transforms', contains a list of items in the XML that need to be updated for the layout to work properly (i.e. setting DISCIPLINE to 'CTC' or 'APB-2') or setting the proper JMRIPREFIX for any DCC decoders so that they work with the layout's DCC system.

```bash
cd Examples
../CATSLayoutGenerator.sh ExampleLayoutAPB.xlsx
```
## Examples Directory

Processed CATS XML files after <B>CATSFileProcessor</B><br/>
<B>CTC_SINGLE_TRACK.xml</B><br/>
<B>CTC_DOUBLE_TRACK.xml</B><br/>
<B>CTC_OS_LEFT.xml</B><br/>
<B>CTC_OS_RIGHT.xml</B><br/>
<B>CTC_XOVR_LEFT.xml</B><br/>
<B>CTC_XOVR_RIGHT.xml</B><br/>
<B>PASSIVE_SINGLE_TRACK.xml</B><br/>
<B>PASSIVE_DOUBLE_TRACK.xml</B><br/>

Example input spreadsheet for <B>CATSFileProcessor</B><br/>
<B>ExampleModuleDefinitions.xlsx</B>

Example input spreadsheet for <B>CATSLayoutGenerator</B><br/>
<B>ExampleLayoutAPB.xlsx</B>:

Example CATS Layout generated by <B>CATSLayoutGenerator</B><br/>
<B>ExampleLayoutAPB.xml</B>

Directory containing the template CATS XML files<br/>
<B>CATSTemplates/</B><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<B>CTC_SINGLE_TRACK.xml</B><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<B>CTC_DOUBLE_TRACK.xml</B><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<B>CTC_OS_LEFT.xml</B><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<B>CTC_OS_RIGHT.xml</B><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<B>CTC_XOVR_LEFT.xml</B><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<B>CTC_XOVR_RIGHT.xml</B><br/>
NOTE: These two files are not copied by <B>CATSFileProcessor</B> because they aren't defined in the spreadsheet--they're passive so they have no elements that need management but they're part of the layout.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<B>PASSIVE_SINGLE_TRACK.xml</B><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<B>PASSIVE_DOUBLE_TRACK.xml</B><br/>

