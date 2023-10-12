import os
import shutil
import zipfile
import tarfile
import platform
import datetime

def backup_directory(source_dir, dest_dir):
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    
    # Check if destination directory exists, create if not
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # List all files in the source directory
    files = os.listdir(source_dir)
    
    # Copy each file from source to destination
    for file in files:
        source_path = os.path.join(source_dir, file)
        dest_path = os.path.join(dest_dir, file)
        
        # Copy the file
        shutil.copy2(source_path, dest_path)
        print(f"Backed up: {source_path} to {dest_path}")

def create_archive(directory_name, archive_type):
    valid_archive_types = ["zip", "gztar", "tar", "bztar", "xztar"]
    if archive_type not in valid_archive_types:
        print("Invalid archive type. Please choose from zip, gztar, tar, bztar, or xztar.")
        return

    home_dir = os.path.expanduser("~")
    directory_path = os.path.join(home_dir, directory_name)

    if not os.path.exists(directory_path):
        print(f"Directory '{directory_name}' does not exist in your home directory.")
        return

    archive_name = f"{directory_name}.{archive_type}"
    with tarfile.open(archive_name, f"w:{archive_type}") as archive:
        archive.add(directory_path, arcname=os.path.basename(directory_name))
    print(f"Archive '{archive_name}' created successfully.")

def check_large_files(zip_file, threshold_kb):
    try:
        zp = zipfile.ZipFile(zip_file)
        size = [[zinfo.filename , zinfo.file_size] for zinfo in zp.filelist ]
        zip_kb = [[name,float(byte_size) / 1000] for name,byte_size in size if (float(byte_size) / 1000)>threshold_kb] # kB

        for name,size in zip_kb:
            print(name,size)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


    except Exception as e:
        print(f"An error occurred: {str(e)}")

def find_recently_modified_files(directory_path="."):
    try:
        current_time = datetime.datetime.now()
        last_month = current_time - datetime.timedelta(days=30)

        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_modified_time > last_month:
                    print(f"{file_path} (Last Modified: {file_modified_time})")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main_menu():
    while True:
        print("\nMenu:")
        print("1. Backup Directory")
        print("2. Create Archive")
        print("3. Check Large Files in Zip Archive")
        print("4. Find Recently Modified Files")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            source_dir = input("Enter the source directory: ")
            dest_dir = input("Enter the destination directory: ")
            backup_directory(source_dir, dest_dir)
        elif choice == "2":
            directory_name = input("Enter the directory name in your home directory: ")
            archive_type = input("Enter the archive type (zip/gztar/tar/bztar/xztar): ")
            create_archive(directory_name, archive_type)
        elif choice == "3":
            zip_file = input("Enter the path to the zip file: ")
            threshold_kb = float(input("Enter the threshold size (KB): "))
            check_large_files(zip_file, threshold_kb)
        elif choice == "4":
            directory_path = input("Enter the directory path (default is current working directory): ")
            find_recently_modified_files(directory_path)
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main_menu()
