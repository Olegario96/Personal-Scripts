import os
import csv

##
## @brief      This functions is very simple. Just take all the files in the
##             current working directory. We check one by one. For those
##             that ends with "_erros.csv" will be put on a list. After
##             that we just return the list.
##
## @return     Return all the csv files that ends with "_erros.csv".
##
def getErrorCsv():
	listCsvError = []

	files = os.listdir(os.getcwd())
	for file in files:
		if str(file).endswith("_erros.csv"):
			listCsvError.append(file)

	return listCsvError

##
## @brief      First of all, we start to iterate in the list that we received
##             from the args. Then, for each element, we create a csv writer
##             and also a csv reader. We create a simple while loop to just
##             eliminate some elements of the header that we don't need to write
##             in our new csv. After that, we iterate line by line in the "old"
##             csv. We check if the line is not empty and have values (that is
##             len(row) > 4). In the first time, we just append the value in
##             the list in form of tuple. In the others interations, we need
##             to check if the tuple isnt already in the list (once the values
##             are not sorted). Finally we call the function 'writeValues' (
##             see its docs. for more info).
##
## @param      listCsvError  The list with the csv files that indicates
##                             which cases have error.
##
## @return     This is a void function.
##
def getCasesFromError(listCsvError):
	i = 0
	setCases = set()

	for file in listCsvError:
		csvFile = open(file, 'r')
		csvOut = open(str(file)+"_erros_new.csv", 'w')

		csvReader = csv.reader(csvFile, delimiter=',', quotechar='|')
		csvWriter = csv.writer(csvOut, delimiter=',', quotechar='|')
		header = csvReader.__next__()

		while i < 3:
			header.pop()
			i += 1

		header.pop(0)
		header.pop(1)
		i = 0


		for row in csvReader:
			if row and len(row) > 4:
				if not setCases:
					tup = (row[1], row[3])
					setCases.add(tup)
				else:
					if (row[1], row[3]) not in setCases:
						tup = (row[1], row[3])
						setCases.add(tup)

		writeValues(list(setCases), header, csvWriter)

##
## @brief      This function write the header in the beginig of the csv. After
##             that, we start to iterate the list and write case by case in our
##             csv.
##
## @param      setCases  The list cases that not converged
##
## @param      header      A simple label list to write in the begining of the
## 						   csv.
##
## @param      csvWriter  The csv writer, responsable for write the content
##
## @return     This is a void function.
##
def writeValues(setCases, header, csvWriter):
	csvWriter.writerow(header)
	for element in setCases:
		csvWriter.writerow(element)

if __name__ == '__main__':
	listCsvError = getErrorCsv()
	getCasesFromError(listCsvError)