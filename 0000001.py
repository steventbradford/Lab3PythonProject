import csv
import os
import subprocess
import random
import time
import argparse

def create_user_account(first_name, last_name, user_group, existing_usernames):
    # Create username
    base_username = (last_name + first_name[0]).lower()
    username = base_username
    suffix = 1
    while username in existing_usernames:
        username = base_username + str(suffix)
        suffix += 1

    # Generate random password
    password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))

    # Add user to group
    subprocess.run(["useradd", "-c", f"{last_name} {first_name}", "-m", "-p", password, username])

    # Add user to the specified group
    subprocess.run(["usermod", "-aG", user_group, username])

    return {'First Name': first_name, 'Last Name': last_name, 'Username': username, 'Password': password}

def main():
    parser = argparse.ArgumentParser(description='Create user accounts based on employee details.')
    parser.add_argument('E_FILE_PATH', help='The path to the employee file name (including the file name)')
    parser.add_argument('OUTPUT_FILE_PATH', help='The path to name of the file to store the employee account details (include the file name)')
    parser.add_argument('-l', '--log', metavar='Logfile_name', help='Append a message to the log file')

    args = parser.parse_args()

    # Log the execution if a log file is provided
    if args.log:
        log_file_path = args.log
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"Program executed at {time.time_ns()}\n")

    # Read existing usernames from /etc/passwd
    existing_usernames = set()
    with open('/etc/passwd', 'r') as passwd_file:
        for line in passwd_file:
            username = line.split(':')[0]
            existing_usernames.add(username)

    # Read employee details from the CSV file
    employee_accounts = []
    with open(args.E_FILE_PATH, 'r') as employee_file:
        reader = csv.DictReader(employee_file)
        for row in reader:
            user_details = create_user_account(row['first_name'], row['last_name'], row['user_group'], existing_usernames)
            employee_accounts.append(user_details)

    # Write employee account details to the output CSV file
    with open(args.OUTPUT_FILE_PATH, 'w', newline='') as output_file:
        fieldnames = ['First Name', 'Last Name', 'Username', 'Password']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(employee_accounts)

if __name__ == "__main__":
    main()
