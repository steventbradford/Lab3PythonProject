import csv

#Write a Python script that includes at least three user-defined functions; one for reading the data from
#the given file, another for creating the new file with suspicious login employee information, and the third
#for calling the other two functions

#function for reading the data in the csv file
def readEmployeeData(file_path):
  employee_data = []
  with open(file_path, 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader) #This skips the header
    for row in csv_reader:
      employee_data.append(row)
    return employee_data
