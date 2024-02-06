import os
import requests

########################################################################################################################
# DESCRIPTION:
# url-checker-cleaner.py is a script designed to audit URLs in text files named "list-*.txt" within the 'urlLists'
# directory. It skips comments, checks each URL for accessibility, and reports any errors. If any URL fails,
# the script removes it and creates a backup of the original file, ensuring only valid URLs remain. This process keeps
# your URL lists clean and up-to-date.
########################################################################################################################

# Path to the folder with the URL lists
directory = 'urlLists'

# Cycle through all files in the directory
for filename in os.listdir(directory):
    # Check whether the file begins with "list-" and ends with ".txt"
    if filename.startswith("list-") and filename.endswith(".txt"):
        path = os.path.join(directory, filename)
        backup_path = path + '.bak'

        # Prepare a list to store the valid URLs
        valid_urls = []
        # Variable to check whether an error was found
        error_found = False

        # Open the file and read each line
        with open(path, 'r') as file:
            for line in file:
                # Ignore comments and blank lines
                if not line.strip().startswith('#') and line.strip():
                    url = line.strip()  # Entferne whitespace von beiden Seiten
                    try:
                        response = requests.head(url, timeout=5)
                        # Check HTTP status code
                        if response.status_code >= 400:
                            print(f'{filename} => {url} returned {response.status_code}')
                            error_found = True
                        else:
                            # If the URL is valid, add it to the list
                            valid_urls.append(line)
                    except requests.RequestException as e:
                        print(f'{filename} => {url} raised an error: {e}')
                        error_found = True
                else:
                    # Add comments and empty lines to the list as they are
                    valid_urls.append(line)

        # If an error is found, create a backup and write back the valid URLs
        if error_found:
            # Create a backup of the original file
            os.rename(path, backup_path)
            # Write the valid URLs (and comments) back into the original file
            with open(path, 'w') as file:
                file.writelines(valid_urls)
