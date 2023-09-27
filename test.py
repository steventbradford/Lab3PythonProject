import os

# Task 1: Implementing methods

def createFiles(fileNamePrefix: str, numOfFiles: int, extension: str):
    for i in range(1, numOfFiles + 1):
        filename = f"{fileNamePrefix}_{i}.{extension}"
        if not os.path.exists(filename):
            open(filename, 'w').close()

def getType(fileOrDirectoryPath: str):
    if os.path.isfile(fileOrDirectoryPath):
        return "File"
    elif os.path.isdir(fileOrDirectoryPath):
        return "Directory"
    else:
        return "Does not exist"

def renameFile(filename: str, newName: str):
    if os.path.exists(filename):
        os.rename(filename, newName)

def createDir(nameOfDirectory: str):
    if not os.path.exists(nameOfDirectory):
        os.makedirs(nameOfDirectory)

def createSubDirectories(directoryName: str, numberToCreate: int):
    for i in range(1, numberToCreate + 1):
        subdir_name = os.path.join(directoryName, f"Subdir_{i}")
        createDir(subdir_name)

def renameFiles(targetDirectory: str, currentExt: str, newExt: str):
    for filename in os.listdir(targetDirectory):
        if filename.endswith(f".{currentExt}"):
            new_filename = filename.replace(f".{currentExt}", f".{newExt}")
            os.rename(os.path.join(targetDirectory, filename), os.path.join(targetDirectory, new_filename))

def displayContents(directoryName: str):
    print(f"{'Name':<40} Type")
    print("-" * 50)
    for item in os.listdir(directoryName):
        item_type = getType(os.path.join(directoryName, item))
        print(f"{item:<40} {item_type}")

# Task 2: main method

def main():
    # a. Print the name of the current directory
    current_directory = os.getcwd()
    print(f"Current Directory: {current_directory}")

    # b. Create a directory under the home directory
    username = os.getlogin()
    new_directory_name = f"CITFall2023{username}"
    home_directory = os.path.expanduser("~")
    cit_directory = os.path.join(home_directory, new_directory_name)
    createDir(cit_directory)

    # c. Print the name of the current directory again
    current_directory = os.getcwd()
    print(f"Current Directory: {current_directory}")

    # d. Prompt user for number of files and their extension
    num_files = int(input("Enter the number of files to create: "))
    extension = input("Enter the file extension (txt, png, doc, dat): ")
    
    # Validate extension
    allowed_extensions = ["txt", "png", "doc", "dat"]
    if extension not in allowed_extensions:
        print("Invalid extension. Allowed extensions are: txt, png, doc, dat")
        return

    createFiles("file", num_files, extension)

    # e. Prompt user for number of subdirectories
    num_subdirectories = int(input("Enter the number of subdirectories to create: "))
    createSubDirectories(cit_directory, num_subdirectories)

    # f. Display contents of the current directory
    displayContents(current_directory)

    # g. Prompt user for a new extension and rename files
    new_extension = input("Enter the new extension for files: ")
    renameFiles(cit_directory, extension, new_extension)

    # h. Display contents of the current directory again
    displayContents(current_directory)

if __name__ == "__main__":
    main(
