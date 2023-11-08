import re
import argparse
import csv

def extract_compromised_records(input_file):
    compromised_records = []
    try:
        with open(input_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # Check if the row has enough columns
                if len(row) >= 4:
                    name, department, email, ip_address = row[:4]
                    # Check if IP address belongs to the compromised subnet
                    if re.match(r'^200\.10\.15\.\d{1,3}$', ip_address):
                        compromised_records.append((name, department, email))
    except Exception as e:
        print(f"Error: {e}")
    return compromised_records

def check_weak_passwords(input_file):
    weak_passwords = []
    try:
        with open(input_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # Check if the row has enough columns
                if len(row) >= 4:
                    name, department, email, password = row[:4]
                    # Check password complexity rules
                    if not (9 <= len(password) <= 13 and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and
                            re.search(r'\d', password) and len(re.findall(r'[#@!%]', password)) >= 2):
                        reasons = []
                        if len(password) < 9 or len(password) > 13:
                            reasons.append("Password length must be between 9 and 13 characters.")
                        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
                            reasons.append("Password must have a combination of upper- and lower-case characters.")
                        if not re.search(r'\d', password):
                            reasons.append("Password must have at least 1 digit.")
                        if len(re.findall(r'[#@!%]', password)) < 2:
                            reasons.append("Password must include at least two occurrences of #@!%.")
                        weak_passwords.append((name, reasons))
    except Exception as e:
        print(f"Error: {e}")
    return weak_passwords

def update_department_names(input_file, output_file):
    updated_records = []
    try:
        with open(input_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # Check if the row has at least 3 columns (Name, Department, Email)
                if len(row) >= 3:
                    name, department, email = row[:3]
                    # Update department name to Finance if it's Accounting
                    if department.lower() == 'accounting':
                        department = 'Finance'
                    updated_records.append((name, department, email))
    except Exception as e:
        print(f"Error: {e}")

    # Write updated records to the new CSV file (empdata-new.csv)
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for record in updated_records:
                writer.writerow(record)
    except Exception as e:
        print(f"Error: {e}")

    # Display names of employees from the Finance Department to the console
    finance_employees = [record[0] for record in updated_records if record[1].lower() == 'finance']
    print("Employees from the Finance Department:")
    print(", ".join(finance_employees))

# Command line argument parser
parser = argparse.ArgumentParser(description="Process employee data based on specified tasks.")
parser.add_argument('-c', '--comp', help="Specify the input CSV file for compromised records.")
parser.add_argument('-p', '--pwd', action='store_true', help="Check weak passwords.")
parser.add_argument('-a', '--accdept', help="Specify the input CSV file for updating department names.")
args = parser.parse_args()

# Check command line arguments and perform the corresponding task
if args.comp:
    compromised_records = extract_compromised_records(args.comp)
    # Save compromised records to a file named compdata.csv
    try:
        with open('compdata.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for record in compromised_records:
                writer.writerow(record)
    except Exception as e:
        print(f"Error: {e}")
elif args.pwd:
    weak_passwords = check_weak_passwords('empdata.csv')
    for record in weak_passwords:
        print(f"Employee: {record[0]}\nWeak Password Reasons: {', '.join(record[1])}\n")
elif args.accdept:
    update_department_names(args.accdept, 'empdata-new.csv')
