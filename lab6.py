import os
import pwd
import crypt
import random
import string

# Function to check if a username exists in the system
def username_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False

# Function to generate a random password
def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Function to create a new user account
def create_user():
    username = input("Enter username: ")
    if username_exists(username):
        print("User already exists.")
        return False
    
    full_name = input("Enter full name: ")
    password = generate_password()
    encrypted_password = crypt.crypt(password, crypt.METHOD_SHA256)
    
    try:
        os.system(f"useradd -m -p {encrypted_password} -c '{full_name}' {username}")
        print(f"User '{username}' created successfully with password: {password}")
        return True
    except Exception as e:
        print(f"Failed to create user: {e}")
        return False

# Function to remove a user account
def remove_user():
    username = input("Enter username to remove: ")
    if not username_exists(username):
        print("User does not exist.")
        return False
    
    try:
        os.system(f"userdel -r {username}")
        print(f"User '{username}' has been removed.")
        return True
    except Exception as e:
        print(f"Failed to remove user: {e}")
        return False

# Function to modify an existing user account
def modify_user():
    username = input("Enter username to modify: ")
    if not username_exists(username):
        print("User does not exist.")
        return False
    
    print("Choose an option:")
    print("1. Lock the account")
    print("2. Change the real name associated with the account")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        os.system(f"passwd -l {username}")
        print(f"Account '{username}' has been locked.")
        return True
    elif choice == "2":
        new_full_name = input("Enter new full name: ")
        try:
            os.system(f"usermod -c '{new_full_name}' {username}")
            print(f"Full name for '{username}' has been changed to '{new_full_name}'.")
            return True
        except Exception as e:
            print(f"Failed to modify user: {e}")
            return False
    else:
        print("Invalid choice.")
        return False

# Main menu function
def main_menu():
    while True:
        print("User Account Management Menu:")
        print("1. Check if username exists")
        print("2. Create a new user")
        print("3. Remove a user")
        print("4. Modify a user account")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username to check: ")
            if username_exists(username):
                print("Username exists.")
            else:
                print("Username does not exist.")
        elif choice == "2":
            create_user()
        elif choice == "3":
            remove_user()
        elif choice == "4":
            modify_user()
        elif choice == "5":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Entry point of the script
if __name__ == "__main__":
    main_menu()
