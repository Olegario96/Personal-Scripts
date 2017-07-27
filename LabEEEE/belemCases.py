import os
import csv

##
## @brief      This function create a list with all files/directories from the
##             dir. "belem". After that, we check if the file is a directory
##             that the name starts with "tip". If so, we put in the list
##             concatening with the number of the typology.
##
## @return     Return a list with the paths to each typology.
##
def getPathsToTips():
	tip = 1
	listTips = []
	listDirectories = os.listdir('belem/')

	listDirectories.sort()
	for directory in listDirectories:
		if str(directory).startswith('tip'+str(tip)):
			listTips.append(directory)

		tip += 1

	return listTips

##
## @brief      Using the function "getPathsToTips" (see its docs. for more
##             info) we have the path for all typologys. After that, we put
##             the file that ends with "erros.csv" in a list inside each
##             folder tip. Then, we return the list
##
## @return     Return the path to all "erros.csv" files inside each tip.
##
def getCsvErrors():
	listCsvErrors = []
	listTips = getPathsToTips();

	for tip in listTips:
		path = "belem/" + tip + "/resultados/"
		files = os.listdir(path)
		for file in files:
			if file.endswith("erros.csv"):
				listCsvErrors.append(path + file)

	return listCsvErrors

##
## @brief      Using the list_csv that we received as argument, we iterate
##             to each element creating a csvReader. We skip the first line
##             (once that has no values) and check if the third column has a
##             value. If so, we append in the list.
##             After do that for each file, we sort the list and return it.
##
## @param      list_csv  The list with the path to all "erros.csv" taken from
##                       'getCsvErrors' (see its docs for more info).
##
## @return     Return a list of tuples with the typology and the id of the case
##             that not converged
##
def errorAnalyze(list_csv):
	tip = 1
	list_erros = []
	for path in list_csv:
		csvFile = open(path, 'r')
		csvReader = csv.reader(csvFile, delimiter=',', quotechar='|')

		csvReader.__next__()
		for row in csvReader:
			if row[2]:
				tup = (tip, row[0])
				list_erros.append(tup)

		tip += 1

	list_erros.sort()
	return list_erros

##
## @brief      We will use the concept of binary search, but instead of return
## 			   the data or the position in our collection we will delete the
## 			   element. (If you don't know the concept of binary search,
## 			   use this link: http://bfy.tw/3rKk)
##
## @param      collection  The collection that we will iterate
## @param      item        The item that we will search by.
##
## @return     This is a void function.
##
def binaryElimination(collection, item):
	first = 0
	last = len(collection) - 1
	found = False
	index = 0

	while first <= last and not found:
	    midpoint = (first + last)//2
	    if collection[midpoint][0] == item:
	        found = True
	    else:
	        if item < collection[midpoint][0]:
	            last = midpoint - 1
	            index = index + 1
	        else:
	            first = midpoint + 1
	            index = index + 1

	collection.pop(midpoint)

##
## @brief      First, we open the file that we want to check, and we
##             transform each line in a element of a list. Then we remove
##             the first (once it has no values) and sort. After that,
##             we use the function "binary_"
##
## @param      casesError  The cases that we get from the "errorAnalyzer"
##                          function (see its doc for more info)
##
## @return     Return the rows from the csv without the cases that not
##             converged.
##
def compareCases(casesError):
	csvFile = open('belem_conforto.csv', 'r')
	csvReader = csv.reader(csvFile, delimiter=',', quotechar='|')
	rows = list(csvReader)
	rows.pop(0)
	rows.sort()
	for error in casesError:
		binaryElimination(rows, error)

	return rows

if __name__ == '__main__':
	csvErrors = getCsvErrors()
	casesError = errorAnalyze(csvErrors)
	rows = compareCases(casesError)

	csvOut = open('belem_conforto_cut.csv', 'w+')
	csvWriter = csv.writer(csvOut, delimiter=',', quotechar='|')

	for row in rows:
		csvWriter.writerow(row)