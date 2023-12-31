
#!/usr/bin/python3
# Asher Applegate, Lab 5

import os
import shutil
import time
import zipfile
import platform

# Task 1: Function to backup files from source directory to destination directory
def backup_directory(source_dir, destination_dir):
    # Checks if source directory exists or not
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    # Checks if destination directory exists or not, creates if not
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        
    # Copies each file from source to destination
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(destination_dir, filename)
        shutil.copy2(source_file, destination_file)
    print(f"Backup from {source_dir} to {destination_dir} completed successfully.")

# Task 2: Function to create archive from a directory
def create_archive(directory_name, archive_type):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    directory_path = os.path.join(desktop_path, directory_name)

    valid_archive_types = ['zip', 'gztar', 'tar', 'bztar', 'xztar']
    if archive_type not in valid_archive_types:
        print("Invalid archive type.")
        return
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return
    
    # Creates the specified type of archive from the provided directory
    shutil.make_archive(os.path.join(desktop_path, directory_name), archive_type, desktop_path, directory_name)
    print(f"Archive '{directory_name}.{archive_type}' created successfully.")

# Task 3: Function to display large files in a zip archive
def display_large_files(zip_file_path, threshold_kb):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for info in zip_ref.infolist():
            file_size_kb = info.file_size / 1024
            if file_size_kb > threshold_kb:
                print(f"File: {info.filename}, OS: {platform.system()}, Size: {file_size_kb:.2f} KB")

# Task 4: Function to display recently modified files in a directory
def display_recently_modified_files(directory_path):
    if not os.path.exists(directory_path):
        directory_path = os.getcwd()

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            modified_time = os.path.getmtime(file_path)
            if time.time() - modified_time < 30 * 24 * 60 * 60:  # Last 30 days
                print(f"File: {file_path}, Last Modified: {time.ctime(modified_time)}")

# Task 5: Menu function to allow the user to interract with the previous functions
def menu():
    while True:
        print("\nMenu:")
        print("[1] Backup Files")
        print("[2] Create Archive")
        print("[3] Display Large Files in Zip Archive")
        print("[4] Display Recently Modified Files")
        print("[5] Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            source_dir = input("Enter source directory: ")
            destination_dir = input("Enter destination directory: ")
            backup_directory(source_dir, destination_dir)
        elif choice == '2':
            directory_name = input("Enter directory name: ")
            archive_type = input("Enter archive type: ")
            create_archive(directory_name, archive_type)
        elif choice == '3':
            zip_file_path = input("Enter path to the zip file: ")
            threshold_kb = float(input("Enter threshold size in KB: "))
            display_large_files(zip_file_path, threshold_kb)
        elif choice == '4':
            directory_path = input("Enter directory path (or press [Enter] for current directory): ")
            display_recently_modified_files(directory_path)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.")

# Menu function to start the program
menu()
