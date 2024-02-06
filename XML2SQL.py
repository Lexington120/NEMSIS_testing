import xml.etree.ElementTree as ET # the preferred lib
import mysql.connector

# Parse the XML file
tree = ET.parse('test.xml')

# Get the root element
root = tree.getroot()

# Prefix to help with legibility
pf = '{http://www.nemsis.org}'


## Moving down the etree
# Extracting header element
header = root.find('*')

# Extracting important demographic data
demographicGroup = header.find(pf + 'DemographicGroup')
agencyElement1 = demographicGroup.find(pf + 'dAgency.01')
agencyID = agencyElement1.text

# Extracting entire EMS dataset
PCR = header.find(pf + 'PatientCareReport')
allElements = PCR.findall('*')

# Creating a list of group names (element tags)
names = []
for index, element in enumerate(allElements):
	# names.append(str(index) + ': ' + element.tag[24:])
	names.append(element.tag[24:])


## SQL Stuff
# Connect to local server and DB
mydb = mysql.connector.connect(
  user="root",
  password="Zj5$q26]}~R6",
  database="CADMUS_DB"
)

# Cursor for executing queries within python script
mycursor = mydb.cursor()

# # Create DC (run once)
# mycursor.execute("CREATE DATABASE CADMUS_DB")

# Delete table
mycursor.execute("DROP TABLE PCR")

# Create table
mycursor.execute("CREATE TABLE PCR (id INTEGER PRIMARY KEY, agency_ID TEXT);")


## Extracting non-PHI PCR data (EMS dataset)
# This grid allows for the masking of data fields -- COLUMN POSITION CORRELATES WITH NUMERICAL VALUE OF THE ELEMENT, INDEXING AT 1 --
mask =  [[1,0,1], # 00 Record
		 [0,1,0]] # 01 Response

# This grid informs of the usage of the field (0:M, 1:R, 2:E, 3:O) -- DO NOT CHANGE --
usage = [[1,0,1],
		 [0,1,0]]

# Variable to stage all of the data in
PCR_data = []

global i
i = 0

# Helper function for data extraction
def extractValues(element,first,current): # Starts with PCR element when inplemented
	subElements = element.findall('*')
	for idx, sele in enumerate(subElements):
		
		# grp manages which data group of the PCR we are in (Record, Response, ...)
		global grp

		if first:
			grp = idx

		# checks if the data element is of the lowest level (they all end in numbers)
		if sele.tag[(25+len(names[grp])):].isnumeric():
			# the row and column wrt the NEMSIS DD
			row = idx
			col = int(sele.tag[(25+len(names[grp])):])

			print('New column created: ' + sele.tag[24:24+len(names[grp])] + sele.tag[25+len(names[grp]):] + '_' + str(idx) + '_' + str(current))
			# create a new column in the SQL table named after the current low-level element
			createColumn(sele.tag[24:24+len(names[grp])] + sele.tag[25+len(names[grp]):] + '_' + str(idx) + '_' + str(current)) # '.' is invalid SQL syntax
			i = i + 1
			print(i)
			# store the value as a string in the PCR_data list
			storeValue(sele,row,col)

		# if not, then extractValues is called recursively on the current sub-element
		else:
			extractValues(sele,0,idx)

# Helper function for data storage
def storeValue(element,row,col):
	value = element.text # this may not work for all values

	if 1: #mask[row][col]: # RESTORE THIS ONCE MASK IS COMPLETE
		# store actual value
		PCR_data.append(value)
	else:
		# store null value
		PCR_data.append('none')

# Create a new column in the SQL table to store the new value
def createColumn(name):
	alter_query = f"ALTER TABLE PCR ADD COLUMN {name} TEXT;"
	mycursor.execute(alter_query)


## Actually run stuff
extractValues(PCR,1,-1)

print(PCR_data)

# Insert values from python variables - only needs to be called once per PCR
sql = "INSERT INTO PCR VALUES (%s, %s, %s, %s, %s, %s)" # TODO: CHANGE TO DYNAMIC SIZING
val = tuple([1, agencyID]) #+ [PCR_data])
mycursor.execute(sql, val)

# Check result
mycursor.execute("SELECT * FROM PCR;")
myresult = mycursor.fetchall()
for x in myresult:
  print(x)

## NEMSIS PCR Data Legend
# 00 Record
# 01 Response
# 02 Dispatch
# 03 Crew
# 04 Times
# 05 Patient
# 06 Payment
# 07 Scene
# 08 Situation
# 09 Injury
# 10 Arrest
# 11 History
# 12 Narrative
# 13 Vitals
# 14 Labs
# 15 Exam
# 16 Protocols
# 17 Medications
# 18 Procedures
# 19 Disposition
# 20 Outcome
# 21 Other