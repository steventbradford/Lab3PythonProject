#!/usr/bin/python3
# Lab 3 Python Project 
# Steven Bradford and Asher Applegate

import os

# Function to validate file extensions
def validate_extension(extension):
    allowed_extensions = ["txt", "png", "doc", "dat"]
    return extension.lower() in allowed_extensions

# Function to validate positive integer input
def validate_positive_integer(input_str):
    try:
        value = int(input_str)
        if value > 0:
            return True, value
    except ValueError:
        pass
    return False, None

# Method 1: createFiles
# This method will create a number of files if they do not exist
# It will accept the parameters fileNamePrefix:str and numOfFiles:int
def createFiles(fileNamePrefix:str, numOfFiles:int, extension:str):
    for i in range(1, numOfFiles + 1):
        filename = f"{fileNamePrefix}_{i}.{extension}"
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write('')
            print(f"File '{filename}' has been created.")
        else:
            print(f"File '{filename}' already exists.")

# Method 2: getType
# This method will return the string "File" if it fileOrDirectoryPath is a file and Directory otherwise
# It will accept the parameters fileOrDirectoryPath:str
def getType(fileOrDirectoryPath:str):
  if os.path.isfile(fileOrDirectoryPath):
    return "File"
  elif os.path.isdir(fileOrDirectoryPath):
    return "Directory"
  else:
    return "Does not exist"

# Method 3: renameFile
# This method will rename a file to the new name
# It will accept the parameters filename:str and newName:str
def renameFile(filename:str, newName:str):
  if os.path.exists(filename):
    new_filename = os.path.join(os.path.dirname(filename), newName)
    os.rename(filename, new_filename)
    print(f"File '{filename}' has been renamed to '{newName}'.")
  else:
    print(f"File '{filename}' does not exist.")

# Method 4: createDir
# This method will create a directory if it does not already exist
# It will accept the parameters nameOfDirectory:str
def createDir(nameOfDirectory:str):
  if not os.path.exists(nameOfDirectory):
    os.mkdir(nameOfDirectory)
    print(f"Directory '{nameOfDirectory}' has been created.")
  else:
    print (f"Directory '{nameOfDirectory}' already exists.")

# Method 5: createSubDirecties
# This method will create numberToCreate subdirectories of the directory directoryName
# It will accept the parameters directoryName:str and numberToCreate:int
def createSubDirectories(directoryName:str, numberToCreate:int):
  for i in range(1, numberToCreate +1):
    subdirectory = os.path.join(directoryName, f"subdir{i}")
    if not os.path.exists(subdirectory):
      os.mkdir(subdirectory)
      print(f"Subdirectory '{subdirectory}' has been created.")
    else:
      print(f"Subdirectory '{subdirectory}' already exists.")

# Method 6: renameFiles
# This method will rename all the files in the target directory with extension currentExt to extenstion newExt.
# It will accept the parameters targetDirectory:str and currentExt:str and newExt:str
def renameFiles(targetDirectory:str, currentExt:str, newExt:str):
    for root, _, files in os.walk(targetDirectory):
        for filename in files:
            if filename.endswith(f".{currentExt}"):
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, filename.replace(f".{currentExt}", f".{newExt}"))
                os.rename(old_path, new_path)
                print(f"File '{filename}' renamed to '{new_path}'.")

# Method 7: displayContents
# This method will display the list of files and directories of the directory. This should display the following table
# It will accept the parameters directoryName:str
def displayContents(directoryName:str):
  print("Name".ljust(50), "Type")
  print("-" * 50, "------")
  for item in os.listdir(directoryName):
    item_path = os.path.join(directoryName, item)
    item_type = getType(item_path)
    print(f"{item.ljust(50)} {item_type}")

# Main method
def main():

    # a. Print the name of the current directory
    current_directory = os.getcwd()
    print(f"Current Directory: {current_directory}")

    # b. Create a directory under the home directory of the current user
    username = os.getlogin()
    user_directory = os.path.expanduser("~")
    cit_directory = os.path.join(user_directory, f"CITFall2023{username}")
    createDir(cit_directory)

    # This was not in the instructions, but had to be added in order for it to work as intended
    os.chdir(cit_directory)
    current_directory = os.getcwd()
    print(f"Changed Current Directory to: {cit_directory}")

    # c. Print the name of the current directory
    print(f"Current Directory: {current_directory}")

    # d. Prompt the user for the number of files and their extension
    while True:
        num_files_input = input("Enter the number of files to create: ")
        valid, num_files = validate_positive_integer(num_files_input)
        if valid:
            break
        else:
            print("Please enter a positive integer for the number of files.")

    extension = input("Enter the file extension (txt, png, doc, or dat): ")
    while not validate_extension(extension):
        extension = input("Invalid extension. Enter a valid extension (txt, png, doc, or dat): ")

    createFiles(f"{cit_directory}/file", num_files, extension)

    # e. Prompt the user for the number of subdirectories to create
    while True:
        num_subdirs_input = input("Enter the number of sub-directories to create: ")
        valid, num_subdirs = validate_positive_integer(num_subdirs_input)
        if valid:
            break
        else:
            print("Please enter a positive integer for the number of sub-directories.")

    createSubDirectories(cit_directory, num_subdirs)
    print(f"Created {num_subdirs} subdirectories in {cit_directory}")

    # f. Display the contents of the current directory
    displayContents(current_directory)

    # g. Prompt the user for a new extension for the files and rename them
    new_extension = input("Enter a new extension for the files (txt, png, doc, or dat): ")
    while not validate_extension(new_extension):
        new_extension = input("Invalid extension. Enter a valid extension (txt, png, doc, or dat): ")

    target_directory = cit_directory
    current_extension = extension
    renameFiles(target_directory, current_extension, new_extension)

    # h. Display the contents of the current directory again
    displayContents(current_directory)
  
if __name__ == "__main__":
    main()
