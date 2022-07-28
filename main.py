# Level Two
import os
from os import walk
from zipfile import ZipFile


class DdosOut:
    def __init__(self):
        self.extract_read()

    # Extract the Zip file and store all the file names in a List from the extracted folder
    def extract_read(self):
        zip_name = input("Please enter the zip file name (including extension eg:- logs.zip) ")
        # Extract Zip File
        with ZipFile(zip_name, 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall()

        filenames = next(walk("./logs"), (None, None, []))[2]  # [] if no file

        self.find_initiator(filenames)

    # Discover which computer initiated the attack
    # Key Concept to know is the DDOS Attack initiator is also a victim itself
    # thus we should look for the computer IP Address that communicated with itself
    def find_initiator(self, filenames):
        # Check if the logs file has been successfully extracted
        if os.path.exists('./logs'):
            # Change the current working directory to search through logs
            os.chdir('./logs')
        else:
            print("logs are not extracted")
            return
        # Loop through the list of text file names
        i = 0
        initiator_ip = ""
        minimum = 9223372036854775807  # Initial MAX large int number
        while i < len(filenames):
            search_ip = filenames[i].split(".txt")[0]

            # opening a text file
            open_file = open(f"{search_ip}.txt", "r")
            # setting flag and index to 0
            flag = 0
            index = 0

            # Loop through the file line by line
            for line in open_file:
                index += 1

                # checking string is present in line or not
                if search_ip in line:
                    flag = 1
                    break

            # checking condition for string found
            # Set the Initiator IP with the oldest moment
            # or with the OUT/IN that started early in the log file
            if flag != 0 and (minimum > index):
                # Store the text file
                initiator_ip = search_ip
                minimum = index

            # closing a file
            open_file.close()
            i += 1

        self.write_output(initiator_ip)

    # Write the output text file with the IP of the computer that started the attack
    def write_output(self, ip) -> None:
        os.chdir('..')
        file_output = open("output.txt", "w")
        file_output.write(ip)
        file_output.close()
        print('Output written to output.txt')


# Call the Initializer
DdosOut()
