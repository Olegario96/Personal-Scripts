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
def get_error_csv():
	list_csv_error = []

	files = os.listdir(os.getcwd())
	for file in files:
		if str(file).endswith("_erros.csv"):
			list_csv_error.append(file)

	return list_csv_error


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
##             are not sorted). Finally we call the function 'write_values' (
##             see its docs. for more info).
##
## @param      list_csv_error  The list with the csv files that indicates
##                             which cases have error.
##
## @return     This is a void function.
##
def get_cases_from_error(list_csv_error):
	i = 0
	list_cases = []

	for file in list_csv_error:
		csv_file = open(file, 'r')
		csv_file_write = open(str(file)+"_erros_new.csv", 'w')

		csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
		csv_writer = csv.writer(csv_file_write, delimiter=',', quotechar='|')

		header = csv_reader.next()

		while i < 3:
			header.pop()
			i += 1

		header.pop(0)
		header.pop(1)
		i = 0


		for row in csv_reader:
			if row and len(row) > 4:
				if not list_cases:
					tup = (row[1], row[3])
					list_cases.append(tup)
				else:
					if (row[1], row[3]) not in list_cases:
						tup = (row[1], row[3])
						list_cases.append(tup)

		write_values(list_cases, header, csv_writer)


##
## @brief      This function write the header in the beginig of the csv. After
##             that, we start to iterate the list and write case by case in our
##             csv.
##
## @param      list_cases  The list cases that not converged
##
## @param      header      A simple label list to write in the begining of the
## 						   csv.
##
## @param      csv_writer  The csv writer, responsable for write the content
##
## @return     This is a void function.
##
def write_values(list_cases, header, csv_writer):
	csv_writer.writerow(header)
	for element in list_cases:
		csv_writer.writerow(element)

list_csv_error = get_error_csv()
get_cases_from_error(list_csv_error)