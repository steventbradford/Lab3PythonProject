#!/usr/bin/env python3
import csv
import subprocess
import time
import argparse

GROUP_MEMBERS = [
    {"bradfords3": "Steven", "id": "Member1_ID"},
    {"name": "Member2 Name", "id": "Member2_ID"},
    
]

def create_user_groups(employee_data):
    # Extract unique user groups from the employee data
    groups = set(employee["user_group"] for employee in employee_data)
    # Create user groups using Linux groupadd command
    for group in groups:
        subprocess.run(["groupadd", group])

def generate_username(employee_data, first_name, last_name):
    # Generate a username based on the provided rules
    base_username = last_name.lower() + first_name.lower()[0]
    usernames = [employee["username"] for employee in employee_data]
    
    if base_username not in usernames:
        return base_username
    else:
        suffix = 1
        while base_username + str(suffix) in usernames:
            suffix += 1
        return base_username + str(suffix)

def create_user_account(username, full_name):
    # Check for duplicate user accounts using /etc/passwd
    existing_users = subprocess.check_output(["cut", "-d:", "-f1", "/etc/passwd"]).decode().splitlines()
    
    if username not in existing_users:
        # Create a new user account using Linux useradd command
        subprocess.run(["useradd", "-c", full_name, username])

def add_user_to_group(username, user_group):
    # Add user to the specified group using Linux usermod command
    subprocess.run(["usermod", "-aG", user_group, username])

def write_to_csv(output_file_path, user_accounts):
    # Write user account details to a CSV file
    with open(output_file_path, mode='w', newline='') as csvfile:
        fieldnames = ["First Name", "Last Name", "Username", "Password"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(user_accounts)

def main(employee_file_path, output_file_path, log_file_name=None):
    # Read employee data from the CSV file
    with open(employee_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        employee_data = list(reader)

    # Create user groups
    create_user_groups(employee_data)

    # Process each employee
    user_accounts = []
    for employee in employee_data:
        first_name = employee["first_name"]
        last_name = employee["last_name"]
        user_group = employee["user_group"]

        # Generate a unique username
        username = generate_username(employee_data, first_name, last_name)

        # Create user account
        create_user_account(username, f"{last_name} {first_name}")

        # Add user to the specified group
        add_user_to_group(username, user_group)

        # Save user account details
        user_accounts.append({
            "First Name": first_name,
            "Last Name": last_name,
            "Username": username,
            "Password": "SomeGeneratedPassword"  # You need to generate or obtain passwords securely
        })

    # Write user account details to CSV file
    write_to_csv(output_file_path, user_accounts)

    # Log execution time if log file specified
    if log_file_name:
        with open(log_file_name, 'a') as log_file:
            log_file.write(f"Script executed at: {time.time_ns()}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Employee Account Creation Script")
    parser.add_argument("E_FILE_PATH", help="Path to the employee file name (including the file name)")
    parser.add_argument("OUTPUT_FILE_PATH", help="Path to the file to which the employee account details are to be stored (including the file name)")
    parser.add_argument("-l", "--log", dest="LOG_FILE_NAME", help="Logfile name")

    args = parser.parse_args()

    main(args.E_FILE_PATH, args.OUTPUT_FILE_PATH, args.LOG_FILE_NAME)
