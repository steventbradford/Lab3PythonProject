import argparse
from ftplib import FTP

def upload_file(ftp, filename):
    try:
        with open(filename, 'rb') as file:
            ftp.storbinary(f"STOR cit383F2023/{filename}", file)
        print(f"{filename} uploaded successfully.")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")

def download_files(ftp, file_extension):
    file_list = []
    ftp.retrlines(f"NLST cit383F2023/*.{file_extension}", file_list.append)
    
    if not file_list:
        print(f"No files with the extension {file_extension} found on VM2.")
    else:
        for file in file_list:
            ftp.retrbinary(f"RETR cit383F2023/{file}", open(file, 'wb').write)
        print(f"Files with extension {file_extension} downloaded successfully.")

def exec_command(ftp, file_type):
    data = []
    ftp.retrlines(f"LIST cit383F2023/*.{file_type}", data.append)
    
    if not data:
        print(f"No files with the extension {file_type} found on VM2.")
    else:
        print(f"List of files with extension {file_type} on VM2:")
        print("===============================================")
        for line in data:
            print(line)
        print("===============================================")

def main():
    parser = argparse.ArgumentParser(description="FTP Client for CIT383 Lab 9")
    parser.add_argument("FTP_SERVER_IP", help="IP address of the FTP server")
    parser.add_argument("-u", "--upload", metavar="filename", help="Upload the specified file to VM2")
    parser.add_argument("-d", "--download", metavar="fileExtension", help="Download files with the specified extension from VM2")
    parser.add_argument("-l", "--list", metavar="fileType", help="List files with the specified extension on VM2")

    args = parser.parse_args()

    ftp = FTP(args.FTP_SERVER_IP)
    ftp.login(user="student", passwd="your_password")  # Replace "your_password" with the actual password

    if args.upload:
        upload_file(ftp, args.upload)
    elif args.download:
        download_files(ftp, args.download)
    elif args.list:
        exec_command(ftp, args.list)

    ftp.quit()

if __name__ == "__main__":
    main()
