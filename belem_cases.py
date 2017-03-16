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
def get_paths_to_tips():
	tip = 1
	list_tips = []
	list_directories = os.listdir('belem/')

	list_directories.sort()

	for directory in list_directories:
		if str(directory).startswith('tip'+str(tip)):
			list_tips.append(directory)

		tip += 1

	return list_tips


##
## @brief      Using the function "get_paths_to_tips" (see its docs. for more
##             info) we have the path for all typologys. After that, we put
##             the file that ends with "erros.csv" in a list inside each
##             folder tip. Then, we return the list
##
## @return     Return the path to all "erros.csv" files inside each tip.
##
def get_csv_erros():
	list_csv_erros = []
	list_tips = get_paths_to_tips();

	for tip in list_tips:
		path = "belem/" + tip + "/resultados/"
		files = os.listdir(path)
		for file in files:
			if file.endswith("erros.csv"):
				list_csv_erros.append(path + file)

	return list_csv_erros


##
## @brief      Using the list_csv that we received as argument, we iterate
##             to each element creating a csv_reader. We skip the first line
##             (once that has no values) and check if the third column has a
##             value. If so, we append in the list.
##             After do that for each file, we sort the list and return it.
##
## @param      list_csv  The list with the path to all "erros.csv" taken from
##                       'get_csv_erros' (see its docs for more info).
##
## @return     Return a list of tuples with the typology and the id of the case
##             that not converged
##
def error_analyze(list_csv):
	tip = 1
	list_erros = []
	for path in list_csv:
		csv_file = open(path, 'r')
		csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')

		csv_reader.next()
		for row in csv_reader:
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
def binary_elimination(collection, item):

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
## @param      cases_error  The cases that we get from the "error_analyzer"
##                          function (see its doc for more info)
##
## @return     Return the rows from the csv without the cases that not
##             converged.
##
def compare_cases(cases_error):
	csv_file = open('belem_conforto.csv', 'r')
	csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
	rows = list(csv_reader)
	rows.pop(0)
	rows.sort()
	for error in cases_error:
		binary_elimination(rows, error)

	return rows



csv_erros = get_csv_erros()
cases_error = error_analyze(csv_erros)

rows = compare_cases(cases_error)

new_csv_file = open('belem_conforto_cut.csv', 'w+')
csv_writer = csv.writer(new_csv_file, delimiter=',', quotechar='|')

for row in rows:
	csv_writer.writerow(row)