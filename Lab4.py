import csv

#Write a Python script that includes at least three user-defined functions; one for reading the data from
#the given file, another for creating the new file with suspicious login employee information, and the third
#for calling the other two functions

#function for reading the data in the csv file
def read_employee_data(file_path):
  employee_data = []
  with open(file_path, 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader) #This skips the header
    for row in csv_reader:
      employee_data.append(row)
    return employee_data

#function to create a file with suspicous login employee information
def employee_suspicous_login(employee_data):
  suspicious_employee = []
  for employee in employee_data:
    name = f"{employee[1]} {employee[2]}" #This gets the first and last name
    login_count = int(employee[3])
    if 'e' in name.lower() or 'i' in name.lower or login_count >= 200:
      login_count_excess = max(0, login_count - 200)
      first_ip = employee[4].split(',')[0] if employee[4] else "N/A"
      suspicious_employees.append([name, first_ip, login_count, login_count_excess])
  return suspicious_employees

#function for creating a file for the suspiction logins
def create_suspicious_employee_file(file_name, suspicious_employees):
    with open(file_name, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['name', 'first IP address', 'login_count', 'login_count_excess'])
        csv_writer.writerows(suspicious_employees)

#main function for calling the other function
def main():
    file_path = 'employee_logins.csv'
    employee_data = read_employee_data(file_path)
    suspicious_employees = find_suspicious_employees(employee_data)
    
    # Generate a file name based on your NKU user ID 
    your_nku_user_id = 'bradfords3'  
    output_file_name = f'{your_nku_user_id}.csv'
    
    create_suspicious_employee_file(output_file_name, suspicious_employees)
    
    # Print suspicious employee data in a table
    print("{:<30} {:<20} {:<15} {:<20}".format("Name", "First IP Address", "Login Count", "Login Count Excess"))
    for employee in suspicious_employees:
        print("{:<30} {:<20} {:<15} {:<20}".format(*employee))
    
    print(f"Total employees with suspicious login attempts: {len(suspicious_employees)}")

if __name__ == "__main__":
    main()








