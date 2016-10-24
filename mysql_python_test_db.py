import MySQLdb
import os
import csv

program_explain = "We gonna try some tests with" 
program_explain += " MySQL, using Python to 'transform' .csv into a database."
# Our .csv file
csv_file = "my_csv.csv"

# Parameters for MySQL
host = "localhost"
user = "root"
passwd = "Acaciadragoons"
database = "python_mysql_test"


# Command to create a specific table
table = """ CREATE TABLE IF NOT EXISTS Pearson (
				name VARCHAR(30) NOT NULL,
				height SMALLINT NOT NULL,
				university VARCHAR(8),
				work SMALLINT
				) """


##
## @brief      Creates a csv file on read and write binary mode
##
## @return     Return the csv created.
##
def create_and_prepare_csv_file():
	print "Creating the .csv file"
		
	csv_file = open("my_csv.csv", 'r+b')

	return csv_file


##
## @brief      Since this .py is a test, we will fill our csv file
##             with a arbitrary data and write down in our file.
##             Using as delmiter the ',' and writing at the first
##             line the 'header'.
##
## @param      csv_file  The csv file that will be written
##
## @return     This is a void function
##
def fill_csv_file_with_some_shit(csv_file):
	csv_writer = csv.writer(csv_file, delimiter = ',', quotechar = '|')
	
	print "Writing the 'header' on csv file"

	csv_writer.writerow(["Name", "Height", "University", "Work"])

	students = []
	students.append(["Gustavo Olegario", 1.81, "UFSC", 1])
	students.append(["Leonardo M.", 1.73, "UDESC", 1])
	students.append(["Marcio", 1.75, "USP", 0])

	for line in students:
		csv_writer.writerow(line)

	print "The data was successfully written!"



##
## @brief      This is our mainly function. First, create a csv reader
## 			   and then, skip the first line (here we assume that the csv
## 			   is arranged like a SQL table. Also, we consider the first
## 			   line as the 'header'). Then, for each line in our csv
## 			   we update de command 'INSERT INTO' and finally we 
## 			   write in our database using as parameter our row.
##
## @param      cursor    The cursor which will write on our database.
## @param      csv_file  The csv file that we will read.
##
## @return     This is a void function
##
def csv_to_mysql(cursor, csv_file):
	csv_reader = csv.reader(csv_file, delimiter = ',', quotechar = '|')
	csv_reader.next()

	print "\nStarting to transfer content from csv file to MySQL.\n"

	for row in csv_reader:
		insert = """INSERT INTO Pearson 
					VALUES (%s, %s, %s, %s) """

		cursor.execute(insert, (row[0], row[1], row[2], row[3]))



print program_explain

# Creates the file if doesn't exists
if not os.path.exists(csv_file):
	csv_file = create_and_prepare_csv_file()
else: 
	csv_file = csv_file = open(csv_file, 'r+b')

print "Filling the csv file with some data"

fill_csv_file_with_some_shit(csv_file)

print "Now we will prepare our database"

db = MySQLdb.connect(host, user, passwd, database)
cursor = db.cursor()

print "Using " + database + " database"

cursor.execute("DROP TABLE IF EXISTS Pearson")

cursor.execute(table)

csv_to_mysql(cursor, csv_file)

db.commit()
db.close()

print "Table created!"
