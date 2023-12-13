import csv
import os
import subprocess
import random
import string
import time
import argparse

def generate_password(length=8):
    """Generate a random password of the given length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def create_user(username, full_name, password):
    """Create a Linux user account."""
    try:
        subprocess.run(["sudo", "useradd", "-m", "-c", full_name, "-p", password, username], check=True)
        print(f"User '{username}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating user '{username}': {e}")

def add_user_to_group(username, group):
    """Add a user to a Linux user group."""
    try:
        subprocess.run(["sudo", "usermod", "-aG", group, username], check=True)
        print(f"User '{username}' added to group '{group}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error adding user '{username}' to group '{group}': {e}")

def process_employee_file(employee_file_path, output_file_path, log_file_path=None):
    """Process the employee file and create user accounts."""
    # Create a dictionary to store username occurrences
    username_occurrences = {}
    
    # Read employee details from the CSV file
    with open(employee_file_path, 'r') as file:
        reader = csv.DictReader(file)
        
        # Process each employee record
        for row in reader:
            first_name = row['first_name']
            last_name = row['last_name']
            user_group = row['user_group']
            
            # Generate username
            base_username = last_name.lower() + first_name.lower()[0]
            username = base_username
            occurrence = username_occurrences.get(base_username, 0)
            
            if occurrence > 0:
                username += str(occurrence)
            
            username_occurrences[base_username] = occurrence + 1
            
            # Generate password
            password = generate_password()
            
            # Create user account
            create_user(username, f'"{last_name} {first_name}"', password)
            
            # Add user to group
            add_user_to_group(username, user_group)
    
    # Write user details to CSV file
    with open(output_file_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['First Name', 'Last Name', 'Username', 'Password'])
        
        for row in reader:
            writer.writerow([row['first_name'], row['last_name'], username, password])
    
    # Log execution time if log file path is provided
    if log_file_path:
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"Script executed at: {time.time_ns()}\n")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Create user accounts for employees.")
    parser.add_argument("E_FILE_PATH", help="Path to the employee file name (including the file name)")
    parser.add_argument("OUTPUT_FILE_PATH", help="Path to the file to store employee account details (including the file name)")
    parser.add_argument("-l", "--log", help="Logfile name")
    
    args = parser.parse_args()
    
    # Execute the script
    process_employee_file(args.E_FILE_PATH, args.OUTPUT_FILE_PATH, args.log)
