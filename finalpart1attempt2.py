import os
import paramiko
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from getpass import getpass

def connect_to_server(ip_address, username, password):
    # Method to establish an SSH connection to the target server
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(ip_address, username=username, password=password)
        return ssh_client
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        return None

def find_affected_files(ssh_client):
    # Method to identify affected files based on the specified criteria
    stdin, stdout, stderr = ssh_client.exec_command(
        "find ~/ -type f -ctime -30 -mtime -7"
    )
    files_list = stdout.read().decode().splitlines()
    return files_list

def display_files(files_list):
    # Method to display the contents of affected files if the option is specified
    for file_path in files_list:
        print(f"Displaying contents of: {file_path}")
        stdin, stdout, stderr = ssh_client.exec_command(f"cat {file_path}")
        print(stdout.read().decode())

def send_email(sender_email, sender_password, recipient_email, files_list, affected_user):
    # Method to send an email with a list of affected files to the CTO
    subject = "Security Alert - Files Compromised"
    body = f"The following files in the home directory of user '{affected_user}' have been compromised:\n\n"
    for file_path in files_list:
        body += f"{file_path}\n"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the smallest affected file
    smallest_file = min(files_list, key=lambda x: os.path.getsize(x))
    with open(smallest_file, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(smallest_file))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(smallest_file)}"'
        msg.attach(part)

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def download_file(ssh_client, file_path, download_path):
    # Method to download the smallest affected file to the specified download path
    sftp = ssh_client.open_sftp()
    remote_file = file_path
    local_file = os.path.join(download_path, os.path.basename(file_path))
    sftp.get(remote_file, local_file)
    sftp.close()
    print(f"Downloaded file to: {local_file}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Script to monitor files impacted by attacks.")
    parser.add_argument("IP_ADDRESS", help="The IP address of the compromised computer.")
    parser.add_argument("USERNAME", help="The username of the user on the affected computer.")
    parser.add_argument("-d", "--disp", action="store_true", help="Display the contents of affected files.")
    parser.add_argument("-e", "--email", dest="RECPT_EMAIL", required=True, help="Email address of the CTO.")
    parser.add_argument("-p", "--path", dest="DOWNLOAD_PATH", help="Download affected files to this path.")
    parser.add_argument("-H", "--help", action="help", help="Show this help message and exit.")

    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Get user password securely
    password = getpass(prompt="Enter password: ")

    # Connect to the server
    ssh_client = connect_to_server(args.IP_ADDRESS, args.USERNAME, password)

    # Find affected files
    files_list = find_affected_files(ssh_client)

    # Display files if option is specified
    if args.disp:
        display_files(files_list)

    # Send email to CTO
    send_email("CTOCIT383@gmail.com", "CTOCIT383", args.RECPT_EMAIL, files_list, args.USERNAME)

    # Download the smallest affected file
    download_path = args.DOWNLOAD_PATH if args.DOWNLOAD_PATH else os.path.expanduser("~")
    download_file(ssh_client, min(files_list, key=lambda x: os.path.getsize(x)), download_path)

    # Close SSH connection
    ssh_client.close()

if __name__ == "__main__":
    main()
