#!/usr/bin/python
# Group 17
# Asher Applegate and Steven Bradford

import csv
import subprocess
import argparse
import time
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os

def generate_random_password(length=8):
    # Generate a random password
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def delete_user_account(username):
    # Delete a user account using the Linux userdel command
    try:
        subprocess.run(["sudo", "userdel", "-r", username], check=True)
        print(f"User account deleted: {username}")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting user account for {username}: {e}")

def delete_group(group):
    # Delete a group using the Linux groupdel command
    try:
        subprocess.run(["sudo", "groupdel", group], check=True)
        print(f"Group deleted: {group}")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting group {group}: {e}")

def expire_passwords(employee_file_path):
    # Force the password of odd-numbered rows to expire
    with open(employee_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for index, row in enumerate(reader, start=1):
            if index % 2 != 0:
                username = row['username']
                try:
                    subprocess.run(["sudo", "chage", "-d", "0", username], check=True)
                    print(f"Password expired for user: {username}")
                except subprocess.CalledProcessError as e:
                    print(f"Error expiring password for {username}: {e}")

def email_credentials(employee_file_path):
    # Email usernames and temporary passwords
    smtp_server = "your_smtp_server"
    smtp_port = 587
    smtp_username = "your_smtp_username"
    smtp_password = "your_smtp_password"
    sender_email = "your_sender_email"

    with open(employee_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row['username']
            email = row['email']
            temp_password = generate_random_password()

            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = email
            message['Subject'] = 'Temporary Password'

            body = f"Your username is: {username}\nYour temporary password is: {temp_password}"
            message.attach(MIMEText(body, 'plain'))

            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_username, smtp_password)
                    server.sendmail(sender_email, email, message.as_string())
                print(f"Credentials emailed to user: {username}")
            except Exception as e:
                print(f"Error emailing credentials to {username}: {e}")

def piped_commands(command1, command2):
    # Execute two Linux commands in sequence and save the results to a text file
    try:
        # Run the first command and capture its output
        output1 = subprocess.check_output(command1, shell=True, text=True)

        # Run the second command, using the output of the first as input
        result = subprocess.check_output(f"{command2} <<< '{output1}'", shell=True, text=True)

        # Get NKU username for file and directory naming
        nku_username = "your_nku_username"  # Replace with your NKU username

        # Create a subdirectory with NKU username
        subdirectory = f"{nku_username}_output"
        os.makedirs(subdirectory, exist_ok=True)

        # Create a file with the specified format and save the results
        result_file = os.path.join(subdirectory, f"{nku_username}_question2_result.txt")
        with open(result_file, 'w') as file:
            file.write(result)

        print(f"Results saved to: {result_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing commands: {e}")

def process_employee_file(employee_file_path, log_file_path, expire_passwords_flag, email_credentials_flag):
    # Process the employee file and delete user accounts and groups
    log_messages = []

    # Read employee details from CSV file
    with open(employee_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_name = row['first_name']
            last_name = row['last_name']
            group = row['user_group']
            email = row['email']

            # Generate a unique username
            base_username = f"{last_name.lower()}{first_name.lower()[0]}"
            username = base_username
            suffix = 1

            while True:
                try:
                    delete_user_account(username)
                except subprocess.CalledProcessError:
                    break

                username = f"{base_username}{suffix}"
                suffix += 1

            delete_group(group)

            # Expire passwords if the option is enabled
            if expire_passwords_flag:
                expire_passwords(employee_file_path)

            # Email credentials if the option is enabled
            if email_credentials_flag:
                email_credentials(employee_file_path)

    # Write log messages to log file
    if log_file_path:
        with open(log_file_path, 'a') as log_file:
            timestamp = time.time_ns()
            log_file.write(f"{timestamp}: Program executed\n")
            for message in log_messages:
                log_file.write(f"{timestamp}: {message}\n")

def main():
    parser = argparse.ArgumentParser(description="Delete user accounts and groups based on employee details.")
    parser.add_argument("E_FILE_PATH", help="The path to the employee file.")
    parser.add_argument("-l", "--log", dest="LOG_FILE_PATH", help="Log file name.")
    parser.add_argument("-t", "--expire-passwords", action="store_true", dest="EXPIRE_PASSWORDS",
                        help="Force the password of odd-numbered rows to expire.")
    parser.add_argument("-q", "--email-credentials", action="store_true", dest="EMAIL_CREDENTIALS",
                        help="Email usernames and temporary passwords to users.")
    parser.add_argument("-c", "--execute-commands", action="store_true", dest="EXECUTE_COMMANDS",
                        help="Execute Linux commands and save results to a text file.")
    parser.add_argument("-H", "--Help", action="help", help="Show this help message and exit.")

    args = parser.parse_args()

    # Process the employee file and delete user accounts and groups
    process_employee_file(args.E_FILE_PATH, args.LOG_FILE_PATH, args.EXPIRE_PASSWORDS, args.EMAIL_CREDENTIALS)

    #
