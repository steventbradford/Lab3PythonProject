import os
import argparse
import getpass
import smtplib
import paramiko
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def get_files_to_monitor(ip_address, username, password):
    # Establish an SSH connection to the target computer
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username=username, password=password)

        # Get the home directory path
        stdin, stdout, stderr = ssh.exec_command('echo $HOME')
        home_directory = stdout.read().decode().strip()

        # Calculate date ranges
        now = datetime.datetime.now()
        one_month_ago = now - datetime.timedelta(days=30)
        one_week_ago = now - datetime.timedelta(days=7)

        # Find files created in the last month but modified in the past week
        command = f'find {home_directory} -type f -newermt {one_month_ago.strftime("%Y-%m-%d")} ! -newermt {one_week_ago.strftime("%Y-%m-%d")}'
        stdin, stdout, stderr = ssh.exec_command(command)
        files = stdout.read().decode().splitlines()

        # Return a list of file paths and their last modified dates
        return files

def display_files(files):
    # Implement code to display the contents of affected files
    for file_path in files:
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"Content of {file_path}:\n{content}\n{'=' * 40}")

def send_email(recipient_email, sender_email, sender_password, files, affected_user):
    # Set up the email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Log in to the sender's email account
    server.login(sender_email, sender_password)

    # Compose the email
    subject = f"File Monitoring Report for {affected_user}"
    body = f"Dear CTO,\n\nThe following files in the home directory of {affected_user} have been identified as potentially compromised:\n\n"
    body += "\n".join(files)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the smallest file
    smallest_file = min(files, key=os.path.getsize)
    with open(smallest_file, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(smallest_file))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(smallest_file)}"'
        msg.attach(part)

    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())

    # Clean up
    server.quit()

def download_file(ssh, file_path, download_path=None):
    # Implement code to download the specified file to the specified directory
    sftp = ssh.open_sftp()
    destination_path = os.path.join(download_path, os.path.basename(file_path)) if download_path else os.path.expanduser("~")
    sftp.get(file_path, destination_path)

def main():
    # Define command-line arguments
    parser = argparse.ArgumentParser(description="File Monitoring Script")
    parser.add_argument("IP_ADDRESS", help="The IP address of the target computer")
    parser.add_argument("USERNAME", help="The username on the affected computer")
    parser.add_argument("-d", "--disp", action="store_true", help="Display the contents of affected files")
    parser.add_argument("-e", "--email", required=True, help="Email address of the CTO")
    parser.add_argument("-p", "--path", help="Download path for affected files")
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")

    # Parse command-line arguments
    args = parser.parse_args()

    if args.help:
        parser.print_help()
        return

    # Get password securely
    password = getpass.getpass(prompt="Enter the password for {}: ".format(args.USERNAME))

    # Get affected files
    files = get_files_to_monitor(args.IP_ADDRESS, args.USERNAME, password)

    # Display files if the option is provided
    if args.disp:
        display_files(files)

    # Send email to the CTO
    send_email(args.email, "CTOCIT383@gmail.com", "CTOCIT#*#", files, args.USERNAME)

    # Establish an SSH connection for file download
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(args.IP_ADDRESS, username=args.USERNAME, password=password)

        # Download the smallest affected file
        smallest_file = min(files, key=os.path.getsize)
        download_path = args.path if args.path else os.path.expanduser("~")
        download_file(ssh, smallest_file, download_path)

if __name__ == "__main__":
    main()
