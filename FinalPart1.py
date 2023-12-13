import os
import paramiko
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta

def connect_to_remote(ip_address, username, password):
    # Establish SSH connection to the remote server
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=username, password=password)
    return ssh

def find_compromised_files(ssh):
    # Get the home directory of the user
    stdin, stdout, stderr = ssh.exec_command('echo $HOME')
    home_directory = stdout.read().decode().strip()

    # Define time thresholds
    current_time = datetime.now()
    one_month_ago = current_time - timedelta(days=30)
    one_week_ago = current_time - timedelta(days=7)

    # Find files created in the last month but modified in the past week
    find_command = f'find {home_directory} -type f -ctime -30 -mtime -7'
    stdin, stdout, stderr = ssh.exec_command(find_command)
    compromised_files = [line.strip() for line in stdout.readlines()]

    return compromised_files

def send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path):
    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Attach body to the email
    message.attach(MIMEText(body, 'plain'))

    # Attach the smallest file to the email
    attachment = open(attachment_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
    message.attach(part)

    # Connect to Gmail SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())

def download_file(ssh, remote_path, local_path='.'):
    # Download the smallest affected file
    sftp = ssh.open_sftp()
    smallest_file = min(sftp.listdir(remote_path), key=lambda x: sftp.stat(os.path.join(remote_path, x)).st_size)
    remote_file_path = os.path.join(remote_path, smallest_file)
    local_file_path = os.path.join(local_path, smallest_file)

    sftp.get(remote_file_path, local_file_path)
    sftp.close()

    return local_file_path

if __name__ == "__main__":
    # Replace these values with your own information
    IP_ADDRESS = input("Enter the target IP address: ")
    USERNAME = input("Enter the target username: ")
    PASSWORD = input("Enter the target password: ")

    # Connect to the remote server
    ssh_connection = connect_to_remote(IP_ADDRESS, USERNAME, PASSWORD)

    # Find compromised files
    compromised_files = find_compromised_files(ssh_connection)

    # Email the CTO
    CTO_EMAIL = input("Enter the CTO's email address: ")
    SENDER_EMAIL = "your.email@gmail.com"
    SENDER_PASSWORD = "your_email_app_password"

    smallest_file_path = download_file(ssh_connection, compromised_files[0])  # Assumes at least one file is found

    subject = "Security Alert: Files Compromised"
    body = f"The following files in the home directory of user {USERNAME} have been compromised:\n\n" \
           f"{', '.join(compromised_files)}"

    send_email(SENDER_EMAIL, SENDER_PASSWORD, CTO_EMAIL, subject, body, smallest_file_path)

    # Close the SSH connection
    ssh_connection.close()
