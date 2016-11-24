import csv

number_lines_complete = 0
number_lines_missing = 0
missing_index = []

def search_for_index(csv_complete, csv_missing):
	global number_lines_complete
	global number_lines_missing

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

def list_to_csv(missing_index):
	csv_padron = open("csv_padron.csv", 'w')
	wr = wr = csv.writer(csv_padron, delimiter=',', quotechar='|')
	for row in missing_index:
		wr.writerow(row)


csv_complete = open("amostratip6.csv", 'rb')
csv_missing = open("miss_cases.csv", 'rb')

search_for_index(csv_complete, csv_missing)

list_to_csv(missing_index)