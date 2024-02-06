import xml.etree.ElementTree as ET # the preferred lib

# Parse the XML file and create an ElementTree
tree = ET.parse('NEMSIS_report.xml')

# Get the root element from the ElementTree
root = tree.getroot()