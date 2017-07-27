import os
import csv
import sqlite3
from pathlib import Path

##
## @brief      This function list all files in the current folder. After that,
##             it will iterate by each file and will test if is a directory
##             (i.e. city). If so, will iterate 6 times, puting the relative
##             path for each tipology of that city into a list. After do this
##             for all cities, will return the list will all paths.
##
## @return     Return a list wich each element is a path that contains the aimed
##             csvs.
##
def pathToAllCsv():
	i = 1
	pathToAllCsv = []
	cities = os.listdir(os.getcwd())

	for city in cities:
		if os.path.isdir(city):
			while i < 7:
				pathToAllCsv.append(city + '/tip' + str(i) + 'nbr/resultados/')
				i += 1
			i = 1

	return pathToAllCsv

##
## @brief      This function remove the strange characters from the csv
##             related to the confort. It will remove the '|[]' chars from the
##             csvs. It will start iterating by each csv file on each folder.
##             It will check if the current file is the confort csv. If so,
##             it will open the file and create a new one to rewrite the file.
##             Then, will iterate for each row on the current csv. For each
##             row will remove the strange characaters and rewrite the row
##             on our new csv file. This processes is repeated for each file
##             on each tipology, on each city.
##
## @param      pathToAllCsv  The path to all csv obtained from the
##             'pathToAllCsv' function. See its documentation for more info.
##
## @return     This is a void function.
##
def fixCsvConf(pathToAllCsv):
	firstTime = True
	charToRemove = set('|[]')

	for path in pathToAllCsv:
		files = os.listdir(path)
		for file in files:
			if str(file).endswith('tempo.csv'):
				csvFile = open(path + file, 'r')
				newCsvFile = open(path + str(file)[:-4] + '_repaired.csv', 'w')
				csvReader = csv.reader(csvFile, delimiter=',')
				csvWriter = csv.writer(newCsvFile, delimiter=',')

				for row in csvReader:
					if not firstTime:
						newRow = [''.join('' if c in charToRemove else c for c in entry) for entry in row]
						csvWriter.writerow(newRow)
					else:
						csvWriter.writerow(row)
						firstTime = False
				csvFile.close()
				firstTime = True

##
## @brief      This function is very similar to the 'fixCsvConf'. But, instead
##             of, remove strange characters, it add two new columns to the
##             csv. It calculate the the total consume of the electricity
##             and calculate the percentage of the confortable hours.
##
## @param      pathToAllCsv  The path to all csv obtained from the
##             'pathToAllCsv' function. See its documentation for more info.
##
## @return     This is a void function.
##
def writeNewValues(pathToAllCsv):
	firstTime = True

	for path in pathToAllCsv:
		files = os.listdir(path)
		for file in files:
			if str(file).endswith('repaired.csv'):
				csvFile = open(path + file,'r')
				newCsvFile = open(path + str(file)[:-4] + '_final.csv', 'w')
				csvReader = csv.reader(csvFile, delimiter=',')
				csvWriter = csv.writer(newCsvFile, delimiter=',')

				for row in csvReader:
					if not firstTime:
						totalConsume = float(row[27]) + float(row[40])
						totalHours = float(row[14])
						newRow = row+[totalConsume, (1-totalConsume/totalHours)]
					else:
						firstTime = False
						aux = [element for element in row if element]
						newRow = (aux + (aux[2:]) * 2 + ['Consumo', 'PHoras'])

					csvWriter.writerow(newRow)
				newCsvFile.close()
				csvFile.close()
				firstTime = True

##
## @brief      This function is responsible for create the query and insert all
##             the data into the database. First, it connects with the
##             'resultadoAnaliseNBR' DB. Then, for each path will list the
##             files and get the current city. Next, evaluates which type csv we
##             dealing (i.e. heating, cooling or confort). After that, uses
##             the function 'createsQuery' to create the query indicating
##             in which table will be used. Finally, open the csv file using
##             the csv reader and insert all the data in the query
##             using a tuple. Then the cursor execute the query for all
##             rows. At the end, just commit the changes and closes the file.
##             The number of the tipology is obtained from the name of the file.
##
## @param      pathToAllCsv  The path to all csv obtained from the function
##                           'pathToAllCsv'. See its documentation for more
##                           info.
##
## @return     This is a void function.
##
def setupQueryAndInsert(pathToAllCsv):
	conn = sqlite3.connect('resultadoAnaliseNBR.db')
	cursor = conn.cursor()

	for path in pathToAllCsv:
		files = os.listdir(path)
		city = Path(path).parts[0]
		for file in files:
			if str(file).endswith("aquecimento.csv"):
				query = createQuery("aquecimento", cursor)
			elif str(file).endswith("resfriamento.csv"):
				query = createQuery("resfriamento", cursor)
			elif str(file).endswith("_final.csv"):
				query = createQuery("conforto", cursor)
			else:
				continue

			csvFile = open(path + file, 'r')
			csvReader = csv.reader(csvFile, delimiter=',')
			csvReader.__next__()

			for row in csvReader:
				tip = int(list(filter(str.isdigit, file))[0])
				params = [city, tip] + row
				finalQuery = query % (tuple(params))
				cursor.execute(finalQuery)

			csvFile.close()
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
	pathToAllCsv = pathToAllCsv()
	fixCsvConf(pathToAllCsv)
	writeNewValues(pathToAllCsv)
	setupQueryAndInsert(pathToAllCsv)