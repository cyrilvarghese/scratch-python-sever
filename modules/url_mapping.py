# url_mapping.py

import json
from urllib.parse import urlparse
from datetime import datetime
import os
# The path to the JSON file that will store the mappings
MAPPING_FILE = '../python-server/util_files/filename_url_mapping.json'

def generate_filename(url):
    path_parts = urlparse(url).path.split('/')
    domain_parts = urlparse(url).netloc.split('.')
    website_name = domain_parts[-2] if len(domain_parts) > 2 else domain_parts[-1]
    domain_extension = domain_parts[-1]
    last_part = path_parts[-1] if path_parts[-1] else path_parts[-2]
    formatted_date = datetime.now().strftime('%d_ %b\'%y')
    filename = f"{website_name}_{formatted_date}_{last_part}.{domain_extension}.txt"
    os.makedirs(os.path.dirname(MAPPING_FILE), exist_ok=True)
    save_mapping(filename, url)
    return filename

def save_mapping(filename, url):
    mappings = load_mappings()
    mappings[filename] = url
    save_mappings(mappings)

def get_original_url(filename):
    mappings = load_mappings()
    return mappings.get(filename)

def load_mappings():
    try:
        with open(MAPPING_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_mappings(mappings):
    with open(MAPPING_FILE, 'w') as file:
        json.dump(mappings, file, indent=4)

if __name__ == "__main__":
    # Test the module functionality
    test_url = 'http://example.com/path/to/resource'
    filename = generate_filename(test_url)
    print(f"Generated filename: {filename}")

    original_url = get_original_url(filename)
    print(f"Original URL: {original_url}")
