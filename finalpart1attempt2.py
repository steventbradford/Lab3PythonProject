import os
import sys
import paramiko
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
import getpass

class FileMonitor:
    def __init__(self, ip_address, username, password, recipient_email, download_path=None, display=False):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.recipient_email = recipient_email
        self.download_path = download_path
        self.display = display

    def connect_to_server(self):
        # Connect to the target server using SSH
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.ip_address, username=self.username, password=self.password)
            return client
        except Exception as e:
            print(f"Error connecting to the server: {e}")
            sys.exit(1)

    def list_affected_files(self, client):
        # List files in the home directory modified in the last month but created in the past week
        cmd = 'find ~ -type f -mtime -30 -ctime -7'
        stdin, stdout, stderr = client.exec_command(cmd)
        files = stdout.read().decode().splitlines()
        return files

    def send_email(self, files):
        # Compose and send an email with the list of affected files
        sender_email = "your.email@gmail.com"  # Replace with your actual email address
        sender_password = "your_email_password"  # Replace with your actual email password

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = "File Monitor Alert"

        body = f"The following files have been compromised on {self.ip_address}:\n\n"
        body += "\n".join(files)
        msg.attach(MIMEText(body, 'plain'))

        # Attach the smallest file
        smallest_file = min(files, key=os.path.getsize)
        attachment = open(smallest_file, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {smallest_file}")
        msg.attach(part)

        # Send email using Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, self.recipient_email, msg.as_string())

    def download_file(self, client, file_path):
        # Download the smallest affected file to the specified path
        sftp = client.open_sftp()
        local_path = os.path.join(self.download_path or os.path.expanduser("~"), os.path.basename(file_path))
        sftp.get(file_path, local_path)
        sftp.close()
        print(f"File downloaded to: {local_path}")

    def display_files(self, files):
        # Display the contents of the affected files
        for file in files:
            with open(file, 'r') as f:
                print(f.read())

    def run(self):
        # Main execution of the script
        client = self.connect_to_server()
        affected_files = self.list_affected_files(client)

        if affected_files:
            print("Affected Files:")
            for file in affected_files:
                print(file)

            if self.display:
                self.display_files(affected_files)

            self.send_email(affected_files)

            if self.download_path:
                self.download_file(client, min(affected_files, key=os.path.getsize))

        else:
            print("No affected files found.")

if __name__ == "__main__":
    # Get user inputs
    ip_address = input("Enter the IP address: ")
    username = input("Enter the username: ")
    password = getpass.getpass("Enter the password: ")
    recipient_email = input("Enter the CTO's email address: ")
    download_path = input("Enter the download path (leave empty for home directory): ")
    display_files = '-d' in sys.argv or '--disp' in sys.argv

    # Create an instance of the FileMonitor class and run the script
    file_monitor = FileMonitor(ip_address, username, password, recipient_email, download_path, display_files)
    file_monitor.run()
