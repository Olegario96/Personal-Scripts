import os
import csv
import sqlite3
from pathlib import Path

##
## @brief      This function just list all files and directories in the current
##             folder. After that, iterate through each element checking if is
##             a 'csv' file and if has the 'tip' string in the name. If so,
##             it appends the file in a list. After do this for each element,
##             returns the list.
##
## @return     All csv related to the typologies.
##
def getAllCsv():
	csvs = []
	files = os.listdir(os.getcwd())
	for file in files:
		if str(file).endswith('.csv') and 'tip' in str(file):
			csvs.append(file)

	return csvs

##
## @brief      This function connects to the our dabase and uses the function
##             'createQuery' to create a generic query base on our target
##             table, which in this case is the 'caracteristicas' table. After
##             that, we open each file from the csvs list using the csv reader.
##             We skip the first line, and for each row of the current csv,
##             we insert all the data in the query and execute it using the
##             cursor. After all this process, we commit the changes and close
##             the database.
##
## @param      csvs  The csvs obtained from the 'getAllCsv' function. See
##                   its documentation for more info.
##
## @return     This is a void funciton.
##
def characteristicsToSQL(csvs):
	conn = sqlite3.connect('../resultadoAnaliseNBR.db')
	cursor = conn.cursor()

	for file in csvs:
		query = createQuery('caracteristicas', cursor)
		csvFile = open(file, 'r')
		csvReader = csv.reader(csvFile, delimiter=',')
		csvReader.__next__()

		for row in csvReader:
			tip = int(list(filter(str.isdigit, file))[0])
			params = [tip] + row
			finalQuery = query % (tuple(params))
			cursor.execute(finalQuery)

	conn.commit()
	conn.close()

##
## @brief      At first, this function performs a 'SELECT' into the database
##             to get the number of rows of this table. The 'SELECT' will be
##             executed on a table depending of the 'typeCsv' parameter.
##             After that, it will start a for loop concatenating a '%s' for
##             each column that the function readed from the table. Finally,
##             it just finalizes the string with a ')' and return the string.
##
## @param      typeCsv  The type csv (can be of type: 'aquecimento',
##             'resfriamento' or 'phoras')
## @param      cursor   The cursor used to execute actions into the database.
##
## @return     Return a query template that will be used to insert new data
##             into our database.
##
def createQuery(typeCsv, cursor):
	firstTime = True
	query = """SELECT * FROM %s """ % (typeCsv)
	templateQuery = """INSERT INTO %s VALUES (""" % (typeCsv)
	names = cursor.execute(query)

	for name in names.description:
		if not firstTime:
			templateQuery += ",'%s' "
		else:
			templateQuery += "'%s'"
			firstTime = False

	templateQuery += ")"
	return templateQuery

if __name__ == '__main__':
	csvs = getAllCsv()
	characteristicsToSQL(csvs)