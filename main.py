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
    print(f"File '{filename}' has been renamed to '{newName}'.")
  else:
    print(f"File '{filename}' does not exist.")

#method 4: createDir
#This method will create a directory if it does not already exist
#It will accept the parameters nameOfDirectory:str
def createDir(nameOfDirectory:str):
  if not os.path.exists(nameOfDirectory):
    os.mkdir(nameOfDirectory)
    print(f"Directory '{nameOfDirectory}' has been created.")
  else:
    print (f"Directory '{nameOfDirectory}' already exists.")

#method 5: createSubDirecties
#This method will create numberToCreate subdirectories of the directory directoryName
#It will accept the parameters directoryName:str and numberToCreate:int
def createSubDirectories(directoryName:str, numberToCreate:int):
  for i in range(1, numberToCreate +1):
    subdirectory = os.path.join(directoryName, f"subdir{i}")
    if not os.path.exists(subdirectory):
      os.mkdir(subdirectory)
      print(f"Subdirectory '{subdirectory}' has been created.")
    else:
      print(f"Subdirectory '{subdirectory}' already exists.")

#method 6: renameFiles
#This method will rename all the files in the target directory with extension currentExt to extenstion newExt.
#It will accept the parameters targetDirectory:str and currentExt:str and newExt:str
def renameFiles(targetDirectory:str, currentExt:str, newExt:str):
  for root, _, files in os.walk(targetDirectory):
    for filename in files:
      if filename.endswith(currentExt):
        old_path = os.path.join(root, filename)
        new_path = os.path.join(root, filename.replace(currentExt, newExt))
        os.rename(old_path, new_path)
        print(f"File '{filename} has been renamed to '{new_path}'.")

#method 7: displayContents
#this method will display the list of files and directories of the directory. This should display the following table
# Name                             Type                
# -----                           --------
#<Name of file or directory       <File or Directory>
#It will accept the parameters directoryName:str
def displayContents(directoryName:str):
  print("Name".ljust(50), "Type")
  print("-" * 50, "------")
  for item in os.listdir(directoryName):
    item_path = os.path.join(directoryName, item)
    item_type = getType(item_path)
    print(f"{item.ljust(50)} {item_type}")

#main method
#this method will accept no parameters and should implement the following task
def main():
      # a. Print the name of the current directory
    current_directory = os.getcwd()
    print(f"Current Directory: {current_directory}")

    # b. Create a directory under the home directory of the current user
    username = os.getlogin()
    user_directory = os.path.expanduser("~")
    cit_directory = os.path.join(user_directory, f"CITFall2023{username}")
    createDir(cit_directory)
    print(f"Created directory: {cit_directory}")

    # c. Print the name of the current directory
    print(f"Current Directory: {current_directory}")

    # d. Prompt the user for the number of files and their extension
    num_files = int(input("Enter the number of files to create: "))
    ext = input("Enter the file extension (txt, png, doc, dat): ")
    while ext not in ["txt", "png", "doc", "dat"]:
        ext = input("Invalid extension. Please enter a valid extension: ")

    createFiles(os.path.join(cit_directory, "file"), num_files)
    print(f"Created {num_files} files with extension {ext} in {cit_directory}")

    # e. Prompt the user for the number of subdirectories to create
    num_subdirs = int(input("Enter the number of subdirectories to create: "))
    while num_subdirs <= 0:
        num_subdirs = int(input("Invalid input. Please enter a positive number of subdirectories: "))

    createSubDirectories(cit_directory, num_subdirs)
    print(f"Created {num_subdirs} subdirectories in {cit_directory}")

    # f. Display the contents of the current directory
    displayContents(current_directory)

    # g. Prompt the user for a new extension for the files and rename them
    new_ext = input("Enter the new file extension (txt, png, doc, dat): ")
    while new_ext not in ["txt", "png", "doc", "dat"]:
        new_ext = input("Invalid extension. Please enter a valid extension: ")

    renameFiles(cit_directory, ext, new_ext)
    print(f"Renamed files with extension {ext} to {new_ext} in {cit_directory}")

    # h. Display the contents of the current directory again
    displayContents(current_directory)
  
if __name__ == "__main__":
    main()
