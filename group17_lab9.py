#!bin/bash/python3
# Group 17
# Lab 9
# Asher Applegate and Steven Bradford

import socket
from ftplib import FTP
import os

# Function to upload a file to VM2
def upload_file(ftp, filename):
    try:
        # Open the file in binary mode and upload it to the specified directory on VM2
        with open(filename, 'rb') as file:
            ftp.storbinary(f"STOR cit383F2023/{filename}", file)
        print(f"{filename} uploaded successfully.")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Function to download files with a specific extension from VM2
def download_files(ftp, file_extension):
    try:
        # Get a list of files with the specified extension on VM2
        files = ftp.nlst(f'cit383F2023/*.{file_extension}')

        # Check if any files were found
        if not files:
            print(f"No files with {file_extension} extension found on VM2.")
            return

        # Download each file to the current working directory on VM1
        for file in files:
            with open(os.path.basename(file), 'wb') as local_file:
                ftp.retrbinary(f"RETR {file}", local_file.write)
            print(f"{os.path.basename(file)} downloaded successfully.")
    except Exception as e:
        print(f"Error downloading files: {e}")

# Function to execute the "ls" command on VM2 and list files of a certain type
def exec_command(ftp, file_type):
    try:
        data = []
        # Get a directory listing of files with the specified type on VM2
        ftp.dir(f'cit383F2023/*.{file_type}', lambda x: data.append(x))

        # Check if any files were found
        if not data:
            print(f"No files with {file_type} extension found on VM2.")
            return

        # Format and print the list of files
        formatted_data = "\n".join(data)
        print(f"Files with {file_type} extension:\n{formatted_data}")
    except Exception as e:
        print(f"Error executing command: {e}")

# Main function
def main():
    try:
        # Get the FTP server IP address and port from the user
        ftp_server_ip = input("Enter FTP server IP: ")
        ftp_server_port = int(input("Enter FTP server port (default is 21): ") or 21)

        # Attempt to establish an FTP connection
        ftp = FTP()
        ftp.connect(ftp_server_ip, ftp_server_port)
        ftp.login("student", "student")

        # Prompt the user to select an option
        choice = input(
            "Select an option:\n1. Upload\n2. Download\n3. List files\nEnter the number corresponding to your choice: ")

        if choice == '1':
            # If the user chose to upload, get the filename and call the upload function
            filename = input("Enter the filename to upload: ")
            upload_file(ftp, filename)
        elif choice == '2':
            # If the user chose to download, get the file extension and call the download function
            file_extension = input("Enter the file extension to download: ")
            download_files(ftp, file_extension)
        elif choice == '3':
            # If the user chose to list files, get the file type and call the exec_command function
            file_type = input("Enter the file type to list: ")
            exec_command(ftp, file_type)
        else:
            # If the user entered an invalid choice, display an error message
            print("Invalid choice. Please enter a valid option.")

        # Close the FTP connection
        ftp.quit()
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
