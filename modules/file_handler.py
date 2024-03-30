# file_handler.py
import os

def write_data_to_file(data, filename="../python-server/files/urls.txt"):
    try:
        # If the directory containing the file doesn't exist, create it
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'a+') as file:
            if os.stat(filename).st_size != 0:
                # If the file exists and is not empty, append data to the end
                file.write('\n' + '\n'.join(data))
                print(f"Data appended to {filename}")
            else:
                # If the file doesn't exist or is empty, write data to it
                file.write('\n'.join(data))
                print(f"Data written to {filename}")

        return True
    except Exception as e:
        print(f"Error writing data to file: {e}")
        return False

def read_data_from_file(filename="../python-server/files/urls.txt"):
    try:
        with open(filename, 'r') as file:
            file_data = file.read()
            urls = list(set(line.strip() for line in file_data.split('\n') if line.strip()))
            print(f"Data read from {filename}")
            return urls
    except Exception as e:
        print(f"Error reading data from file: {e}")
        return []
