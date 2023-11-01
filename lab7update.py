#!bin/bash/python3
# Group 17
# Asher Applegate and Steven Bradford

# Example command: python lab7.py -i output.log -d path/to/directory
# Example command: python lab7.py -h

import os
import argparse

def list_directory_contents(directory, log_file=None, list_directories=False):
    try:
        entries = os.listdir(directory)
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        if log_file:
            with open(log_file, 'a') as log:
                log.write(f"Error: Directory '{directory}' not found.\n")
        return
    
    entries = [entry for entry in entries if entry not in ['.', '..']]
    if list_directories:
        entries = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]
    
    if log_file:
        with open(log_file, 'w') as log:
            log.write(f"File/Dir #\t\tName\n")
            log.write("******\t\t******\n")
            for idx, entry in enumerate(entries, start=1):
                log.write(f"{idx}\t\t\t{entry}\n")
        print(f"Directory contents listed in '{log_file}'")
    else:
        print(f"File/Dir #\t\tName")
        print("******\t\t******")
        for idx, entry in enumerate(entries, start=1):
            print(f"{idx}\t\t\t{entry}")

def main():
    parser = argparse.ArgumentParser(description="List contents of a directory.")
    parser.add_argument('directory', metavar='DIR_PATH', type=str, help='Path of the directory to be listed')
    parser.add_argument('-i', '--logfile', metavar='LOG_FILE', type=str, help='Output to log file')
    parser.add_argument('-d', '--dir', action='store_true', help='List only directories')
    args = parser.parse_args()

    try:
        list_directory_contents(args.directory, args.logfile, args.dir)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
