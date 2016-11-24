import csv

# Total lines of the .csv
number_lines_complete = 0
# Rows to be written at the end
missing_index = []


##
## @brief      We use this function to search every element of de csv_missing
## 			   on the csv_complete file. For do this, we use a binary search
## 			   to accelarate the process. We skip the first line, because
## 			   the first line of complete file is like a 'header'. We
## 			   transform our csv into a list, so this can be done more
## 			   easily.
##
## @param      csv_complete  The complete csv with all information
## @param      csv_missing   The csv with the missing data to be searched on the
## 							 csv_complete
##
## @return     This is a void function
##
def search_for_index(csv_complete, csv_missing):
	global number_lines_complete

	csv_complete.seek(0)
	csv_missing.seek(0)

	csv_complete_reader = csv.reader(csv_complete, delimiter = ',', quotechar = '|')
	csv_missing_reader = csv.reader(csv_missing, delimiter = ',', quotechar = '|')

	csv_complete_reader.next()

	list_complete = list(csv_complete_reader)
	number_lines_complete = len(list_complete)

	for row in csv_missing_reader:
		index = binary_search(list_complete, row[0])
		missing_index.append(index)


##
## @brief      A normal binary search that returns the element. The
## 			   complexity is O(n). If you have doubts what is binary search,
## 			   google it ;).
##
## @param      collection  The collection that will be investigated
## @param      item        The item to be searched
##
## @return     Return the element found
##
def binary_search(collection, item):
	global number_lines_complete

	first = 0
	last = number_lines_complete - 1
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

	return collection[midpoint]


##
## @brief      We just write every element on the list in a csv file
## 			   called "csv_padron"
##
## @param      missing_index  The missing index to be written in the csv
##
## @return     This is a void function
##
def list_to_csv(missing_index):
	csv_padron = open("csv_padron.csv", 'w')
	wr = wr = csv.writer(csv_padron, delimiter=',', quotechar='|')
	for row in missing_index:
		wr.writerow(row)


csv_complete = open("amostratip6.csv", 'rb')
csv_missing = open("miss_cases.csv", 'rb')

search_for_index(csv_complete, csv_missing)

list_to_csv(missing_index)