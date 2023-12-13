#!/usr/bin/python
# Group 17
# Asher Applegate and Steven Bradford

# This script deletes users and groups based on the names of the employees and the groups in the defined file. 
# The usernames are created based on the syntax “[last name][first letter of first name][N]” with N being either blank or a value, starting with 1 and increasing by 1 for each duplicate username, depending on if a user with that username already exists.  
# The script deletes the corresponding users and groups as defined in the employee file. 

# Example command: python ./final_proj_17_part2.py /home/student/employee-f23.csv

import csv
import subprocess
import argparse
import time

def delete_user_account(username):
    # Delete a user account using the Linux userdel command
    try:
        subprocess.run(["sudo", "userdel", "-r", username])
        print(f"User account deleted: {username}")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting user account for {username}: {e}")

def delete_group(group):
    # Delete a group using the Linux groupdel command
    try:
        subprocess.run(["sudo", "groupdel", group])
        print(f"Group deleted: {group}")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting group {group}: {e}")

def process_employee_file(employee_file_path, log_file_path):
    # Process the employee file and delete user accounts and groups
    log_messages = []

    # Read employee details from CSV file
    with open(employee_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_name = row['first_name']
            last_name = row['last_name']
            group = row['user_group']

            # Generate a unique username
            base_username = f"{last_name.lower()}{first_name.lower()[0]}"
            username = base_username
            suffix = 1

            while True:
                try:
                    subprocess.run(["sudo", "userdel", "-r", username], check=True)
                    print(f"User account deleted: {username}")
                except subprocess.CalledProcessError:
                    break

                username = f"{base_username}{suffix}"
                suffix += 1

            try:
                subprocess.run(["sudo", "groupdel", group], check=True)
                print(f"Group deleted: {group}")
            except subprocess.CalledProcessError:
                pass

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
    parser.add_argument("-H", "--Help", action="help", help="Show this help message and exit.")

    args = parser.parse_args()

    # Process the employee file and delete user accounts and groups
    process_employee_file(args.E_FILE_PATH, args.LOG_FILE_PATH)

if __name__ == "__main__":
    main()
