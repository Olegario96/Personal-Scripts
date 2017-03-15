import sys
import os
import csv
import copy

##
## @brief      This function, receive all files from a folder and just return
## 			   the files that have the extension ".epw"
##
## @param      files  The files to be checked
##
## @return     Return a list with all the epw files.
##
def take_epw(files):
	epw_files = []

	for file in files:
		if str(file).endswith(".epw"):
			epw_files.append(file)

	return epw_files

##
## @brief      This function, receive all files from a folder and just return
## 			   the files that have the extension ".idf"
##
## @param      files  The files to be checked
##
## @return     Return a list with all the idf files.
##
def take_idf(files):
	idf_files = []

	for file in files:
		if str(file).endswith(".idf"):
			idf_files.append(file)

	return idf_files

##
## @brief      This function open all epw files in the working directory
##             as a csv. Next, we start to read line by line until we found
##             the row that starts with "GROUND" (this is the place that have
##             the values we want). Then, we look for the number 2 and skip 3
##             elements due to the struct of the epw file. Finally, we just
##             put the 12 temperatures from the epw on a list. We do this for
##             all epw files in our folder and transform from string to float
##             all the values and return then.
##
## @return     Return the 12 * (number of epw files) temperatures
##
def take_epw_values():
	temperatures = []
	temperatures_aux = []
	go = 3
	months = 12
	found = False

	files = os.listdir(os.getcwd())
	files.sort()
	files = take_epw(files)

	for file in files:
		csv_file = open(file, 'r')
		csv_reader = csv.reader(csv_file, delimiter=',', quotechar= '|')

		for row in csv_reader:
			if row[0].startswith("GROUND"):
				for element in row:
					if element == str(2):
						found = True
						continue
					else:
						if found:
							if go == 0:
								if months > 0:
									temperatures.append(element)
									months -= 1
									continue
								else:
									break
							else:
								go -= 1
								continue
						else:
							continue
			else:
				continue

		go = 3
		months = 12
		found = False

	for temp in temperatures:
		temperatures_aux.append(float(temp))

	return temperatures_aux


##
## @brief      First, we open the idf file and create a new file to write
##             the changes that we want to each epw that we read before.
##             We start to read line by line from the idf file until we found
##             the line that starts with "Site:GroundTemperature", so we know
##             that the next line has the values that we need do rewrite. Then,
##             in the next 12 lines we delete the values, just writing ''. After
##             that we write our values of temperature and end the write writing
##             a ';' just to indicate to the idf that  values are ended.
##             Finally, we just restart the variables and eliminate the values
##             that we already wrote. The process repeat for each idf file in
##             the folder. Also, we are using a 'tmp' variable using the copy
##             function just to garantee that the we have a real copy, not a
##             reference, so in the end, when we switch among idf's we
##             will be able to write the same values in new idf's.
##
## @param      temperatures  Temperatures returned from the "take_epw_values"
##                           function. See its doc to more info.
##
## @return     This is a void function
##
def change_idf(temperatures):
	tmp = copy.copy(temperatures)
	i = 0
	j = 0
	months = 12
	limit = (len(temperatures) / months)
	site = False
	wrote_semicolon = False

	files = os.listdir(os.getcwd())
	files.sort()
	names = take_epw(files)
	files = take_idf(files)


	for file in files:
		file_read = open(file, 'r')
		lines = file_read.readlines()
		while i < limit:
			file_write = open(str(file)[:-4]+'_changed_'+names[i]+'.idf', 'w')
			for line in lines:
				if line.startswith("Site:GroundTemperature"):
					site = True
				else:
					if site:
						if months > 0:
							file_write.write('')
							months -= 1
							continue
						else:
							if not wrote_semicolon:
								while j < 12:
									file_write.write(str(temperatures[j]))
									j += 1
									if j < 12:
										file_write.write(',')
								file_write.write(';')
								wrote_semicolon = True

				file_write.write(line)

			i += 1
			months = 12
			site = False
			wrote_semicolon = False
			del temperatures[:j]
			j = 0

		i = 0
		temperatures = copy.copy(tmp)


temperatures = take_epw_values()
change_idf(temperatures)