import socket
from ftplib import FTP
import httplib
import os

def upload_file(ftp, filename):
    try:
        with open(filename, 'rb') as file:
            ftp.storbinary(f"STOR cit383F2023/{filename}", file)
        print(f"{filename} uploaded successfully.")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")

def download_files(ftp, file_extension):
    files = ftp.nlst(f'cit383F2023/*.{file_extension}')
    if not files:
        print(f"No files with {file_extension} extension found on VM2.")
        return

    for file in files:
        with open(os.path.basename(file), 'wb') as local_file:
            ftp.retrbinary(f"RETR {file}", local_file.write)
        print(f"{os.path.basename(file)} downloaded successfully.")

def exec_command(ftp, file_type):
    data = []
    ftp.dir(f'cit383F2023/*.{file_type}', lambda x: data.append(x))
    
    if not data:
        print(f"No files with {file_type} extension found on VM2.")
        return

    # Format the list of files, you may choose to use a table or other format
    formatted_data = "\n".join(data)
    print(f"Files with {file_type} extension:\n{formatted_data}")

def main():
    ftp_server_ip = input("Enter FTP server IP: ")
    ftp = FTP(ftp_server_ip)

    # Log in to the FTP server (assuming username and password are the same for simplicity)
    ftp.login("student", "password")

    choice = input("Select an option:\n1. Upload\n2. Download\n3. List files\nEnter the number corresponding to your choice: ")

    if choice == '1':
        filename = input("Enter the filename to upload: ")
        upload_file(ftp, filename)
    elif choice == '2':
        file_extension = input("Enter the file extension to download: ")
        download_files(ftp, file_extension)
    elif choice == '3':
        file_type = input("Enter the file type to list: ")
        exec_command(ftp, file_type)
    else:
        print("Invalid choice. Please enter a valid option.")

    ftp.quit()

if __name__ == "__main__":
    main()
