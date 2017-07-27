import csv

##
## @brief      We use this function to search every element of de csvMissing
## 			   on the csvComplete file. For do this, we use a binary search
## 			   to accelarate the process. We skip the first line, because
## 			   the first line of complete file is like a 'header'. We
## 			   transform our csv into a list, so this can be done more
## 			   easily.
##
## @param      csvComplete  The complete csv with all information
## @param      csvMissing   The csv with the missing data to be searched on the
## 							 csvComplete
##
## @return     This is a void function
##
def searchForIndex(csvComplete, csvMissing):
	csvComplete.seek(0)
	csvMissing.seek(0)

	csvCompleteReader = csv.reader(csvComplete, delimiter=',', quotechar='|')
	csvMissingReader = csv.reader(csvMissing, delimiter=',', quotechar='|')

	csvCompleteReader.next()

	listComplete = list(csvCompleteReader)
	numberLinesComplete = len(listComplete)

	for row in csvMissingReader:
		index = binarySearch(listComplete, row[0], numberLinesComplete)
		missinIndex.append(index)

##
## @brief      A normal binary search that returns the element. The
## 			   complexity is O(logn). If you have doubts what is binary search,
## 			   google it ;).
##
## @param      collection  The collection that will be investigated
## @param      item        The item to be searched
##
## @return     Return the element found
##
def binarySearch(collection, item, numberLinesComplete):
	first = 0
	last = numberLinesComplete - 1
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
## 			   called "csvPadron"
##
## @param      missinIndex  The missing index to be written in the csv
##
## @return     This is a void function
##
def listToCsv(missinIndex):
	csvPadron = open("csvPadron.csv", 'w')
	wr = wr = csv.writer(csvPadron, delimiter=',', quotechar='|')
	for row in missinIndex:
		wr.writerow(row)
		
if __name__ == '__main__':
	# Total lines of the .csv
	numberLinesComplete = 0
	# Rows to be written at the end
	missinIndex = []
	csvComplete = open("amostratip6.csv", 'rb')
	csvMissing = open("miss_cases.csv", 'rb')

	searchForIndex(csvComplete, csvMissing)
	listToCsv(missinIndex)
