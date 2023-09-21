#Lab 3 Python project 
#Steven Bradford and Asher Applegate

import os

#methods

#method 1: createFiles
#This method will create a number of files if they do not exist
#It will accept the parameters fileNamePrefix:str and numOfFiles:int
def createFiles(fileNamePrefix:str, numOfFiles:int):
  for i in range (1, numOfFiles +1):
    filename = f"{fileNamePrefix}_{i}.txt"
    if not os.path.exists(filename):
      with open(filename, 'w') as file:
        file.write('')
      print(f"File '{filename}' has been created.")
    else:
      print(f"File '{filename}' already exists.")

#method 2: getType
#This method will return the string "File" if it fileOrDirectoryPath is a file and Directory otherwise
#It will accept the parameters fileOrDirectoryPath:str
def getType(fileOrDirectoryPath:str):
  if os.path.isfile(fileOrDirectoryPath):
    return "File"
  elif os.path.isdir(fileOrDirectoryPath):
    return "Directory"
  else:
    return "Does not exist"

#method 3: renameFile
#This method will rename a file to the new name
#It will accept the parameters filename:str and newName:str
def renameFile(filename:str, newName:str):
  if os.path.exists(filename):
    new_filename = os.path.join(os.path.dirname(filename), newName)
    os.rename(filename, new_filename)
    print(f"File '{filename}' has been renamed to '{newName'.")
  else:
    print(f"File '{filename}' does not exist.")

#method 4: createDir
#This method will create a directory if it does not already exist
#It will accept the parameters nameOfDirectory:str

#method 5: createSubDirecties
#This method will create numberToCreate subdirectories of the directory directoryName
#It will accept the parameters directoryName:str and numberToCreate:int

#method 6: renameFiles
#This method will rename all the files in the target directory with extension currentExt to extenstion newExt.
#It will accept the parameters targetDirectory:str and currentExt:str and newExt:str

#method 7: displayContents
#this method will display the list of files and directories of the directory. This should display the following table
# Name                             Type                
# -----                           --------
#<Name of file or directory       <File or Directory>
#It will accept the parameters directoryName:str

#main method
#this method will accept no parameters and should implement the following task
def main():
  username = os.getLogin()
  os.chdir("//home//" + username)
  current_directory = os.getcwd()
  print(current_directory)





