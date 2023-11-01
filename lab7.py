import argparse
import os

def list_directory_contents(dir_path, log_file=None, list_directories=False):
    try:
        with open(log_file, 'w') if log_file else open(os.devnull, 'w') as output:
            entries = os.listdir(dir_path)

            if not list_directories:
                entries = [entry for entry in entries if os.path.isfile(os.path.join(dir_path, entry))]

            if log_file:
                print("File/Dir # Name", file=output)
                print("******** ************************", file=output)

            for i, entry in enumerate(entries, start=1):
                print(f"{i} {entry}")

    except FileNotFoundError:
        if log_file:
            print("Error: The specified directory was not found.", file=output)
        else:
            print("Error: The specified directory was not found.")

def main():
    parser = argparse.ArgumentParser(description="List the contents of a directory")
    parser.add_argument("DIR_PATH", help="The directory path to list contents from")
    parser.add_argument("-i", "--logfile", help="Log file name")
    parser.add_argument("-d", "--dir", action="store_true", help="List only directories")
    parser.add_argument("-h", "--help", action="store_true", help="Display usage information")

    args = parser.parse_args()

    if args.help:
        parser.print_usage()
        return

    if not os.path.exists(args.DIR_PATH):
        print("Error: The specified directory was not found.")
        return

    list_directory_contents(args.DIR_PATH, args.logfile, args.dir)

if __name__ == "__main__":
    main()
