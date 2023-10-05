import csv

# Function to read data from the given CVS file
def read_employee_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip header row
        records = []
        for row in reader:
            records.append(row)
    return records

# Function to determine employees with suspicious login attempts
def create_suspicious_login_file(records, user_id):
    suspicious_employees = []
    for record in records:
        first_name, last_name, _, total_logins, ip_addresses = record
        total_logins = int(total_logins)
        if total_logins >= 200 and ('e' in last_name.lower() or 'i' in last_name.lower()):
            ip_list = ip_addresses.split(',')
            first_ip_address = ip_list[0].strip()
            login_count_excess = total_logins - 200
            suspicious_employees.append([f"{first_name} {last_name}", first_ip_address, total_logins, login_count_excess])

    # Create a new CSV file with suspicious employee login information
    output_file_path = f"{user_id}.csv"
    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'first IP address', 'login_count', 'login_count_excess'])
        writer.writerows(suspicious_employees)
    
    return output_file_path, suspicious_employees

# Function to print suspicious employee information in a table and total number of suspicious employees
def print_suspicious_employees_info(suspicious_employees):
    print("\nSuspicious Employee Login Attempts:")
    print("{:<20} {:<20} {:<15} {:<15}".format('Name', 'First IP Address', 'Login Count', 'Excess Count'))
    print("-" * 70)
    for employee in suspicious_employees:
        print("{:<20} {:<20} {:<15} {:<15}".format(employee[0], employee[1], employee[2], employee[3]))
    print("-" * 70)
    print(f"Total employees with suspicious login attempts: {len(suspicious_employees)}\n")

# Main function that calls other functions
def main():
    file_path = "employee_logins.csv"
    user_id = "applegatea4"
    
    # Read data from the file
    records = read_employee_data(file_path)
    
    # Identify suspicious login attempts and create a new file
    output_file, suspicious_employees = create_suspicious_login_file(records, user_id)
    
    # Print suspicious employee information
    print_suspicious_employees_info(suspicious_employees)
    
    print(f"New file '{output_file}' created with suspicious employee login information.")

# Call the main function to execute the script
if __name__ == "__main__":
    main()
