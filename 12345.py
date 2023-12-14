#!/usr/bin/python
# Group 17

# This script creates users and groups based on the names of the employees and the groups in the defined file.
# The usernames will be created based on the syntax “[last name][first letter of first name][N]” with N being either blank or a value, starting with 1 and increasing by 1 for each duplicate username, depending on if a user with that username already exists.
# The users will be added to the corresponding groups as defined in the employee file.
# The First Name, Last Name, Username, and Password generated will be written to the CSV file that is defined.

# Example command: python ./final_proj_17_part2.py /home/student/employee-f23.csv /home/student/useraccounts.csv

import csv
import subprocess
import os
import argparse
import time
import random
import string

def generate_username(first_name, last_name, existing_usernames):
    # Generate a unique username based on the first and last name
    base_username = f"{last_name.lower()}{first_name.lower()[0]}"
    username = base_username
    suffix = 1

    while username in existing_usernames:
        username = f"{base_username}{suffix}"
        suffix += 1

    return username

def generate_password():
    # Generate a random password
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def create_group(group):
    # Check if the group already exists
    try:
        subprocess.run(["getent", "group", group], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        # Group does not exist, create it
        try:
            subprocess.run(["sudo", "groupadd", group])
            print(f"Group created: {group}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating group {group}: {e}")

def create_user_account(username, full_name, group):
    # Check for duplicate user accounts
    if check_duplicate_user(username):
        print(f"Duplicate user account found: {username}")
        return

    # Generate a random password
    password = generate_password()

    # Create a user account using the Linux useradd command
    try:
        subprocess.run(["sudo", "useradd", "-m", "-c", full_name, "-p", password, username], check=True)
        print(f"User account created: {username}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating user account for {username}: {e}")
        return

    # Create user group if it does not exist
    create_group(group)

    # Add user to the group
    try:
        subprocess.run(["sudo", "usermod", "-aG", group, username], check=True)
        print(f"User added to group: {group}")
    except subprocess.CalledProcessError as e:
        print(f"Error adding user to group {group}: {e}")

def force_password_change(username):
    # Force password change for odd-numbered rows
    try:
        subprocess.run(["sudo", "chage", "-d", "0", username], check=True)
        print(f"Password change forced for user: {username}")
    except subprocess.CalledProcessError as e:
        print(f"Error forcing password change for user {username}: {e}")

def email_password(username, email, password):
    # Your code to send an email
    print(f"Email sent to {email}: Your username is {username} and temporary password is {password}")

def check_duplicate_user(username):
    # Check if the username already exists in /etc/passwd
    try:
        subprocess.run(["grep", username, "/etc/passwd"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def process_employee_file(employee_file_path, output_file_path, log_file_path, force_change=False, email_users=False):
    # Process the employee file and create user accounts
    existing_usernames = set()
    log_messages = []

    # Read employee details from CSV file
    with open(employee_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_name = row['first_name']
            last_name = row['last_name']
            group = row['user_group']
            email = row.get('email')  # Check if 'email' column is present in the CSV

            # Generate a unique username
            username = generate_username(first_name, last_name, existing_usernames)

            # Create user account
            create_user_account(username, f"{last_name} {first_name}", group)

            # Check for force password change option
            if force_change and int(row.get('N', 1)) % 2 != 0:
                force_password_change(username)

            existing_usernames.add(username)

            # Check for email option and send email
            if email_users and email:
                password = generate_password()
                email_password(username, email, password)

    # Write user account details to CSV file
    with open(output_file_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['First Name', 'Last Name', 'Username', 'Password'])
        for username in existing_usernames:
            try:
                full_name = subprocess.check_output(["grep", username, "/etc/passwd"], stderr=subprocess.DEVNULL).decode().split(":")[4]
                first_name, last_name = full_name.strip().split(' ', 1)
                password = generate_password()
                writer.writerow([first_name, last_name, username, password])
            except subprocess.CalledProcessError:
                print(f"Error: User {username} not found in /etc/passwd")

    # Write log messages to log file
    if log_file_path:
        with open(log_file_path, 'a') as log_file:
            timestamp = time.time_ns()
            log_file.write(f"{timestamp}: Program executed\n")
            for message in log_messages:
                log_file.write(f"{timestamp}: {message}\n")

def main():
    parser = argparse.ArgumentParser(description="Create user accounts based on employee details.")
    parser.add_argument("E_FILE_PATH", help="The path to the employee file.")
    parser.add_argument("OUTPUT_FILE_PATH", help="The path to the output file.")
    parser.add_argument("-l", "--log", dest="LOG_FILE_PATH", help="Log file name.")
    parser.add_argument("-t", "--force-change", action="store_true", help="Force password change for odd-numbered rows.")
    parser.add_argument("-q", "--email-users", action="store_true", help="Email usernames and temporary passwords.")
    parser.add_argument("-H", "--Help", action="help", help="Show this help message and exit.")

    args = parser.parse_args()

    # Process the employee file and create user accounts
    process_employee_file(args.E_FILE_PATH, args.OUTPUT_FILE_PATH, args.LOG_FILE_PATH, args.force_change, args.email_users)

if __name__ == "__main__":
    main()
