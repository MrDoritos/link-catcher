import sys
import subprocess
from urllib.parse import urlparse
import tldextract
import mediafire_dl
import mimetypes
import random
import string
import os

def extract_directory(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    directory = ''.join(path.split('/')[:-1])
    return directory

def generate_file_extension(file_path):
    # Get the MIME type of the file
    mime_type, _ = mimetypes.guess_type(file_path)

    # Extract the file extension from the MIME type
    if mime_type:
        _, extension = mime_type.split('/')
        return '.' + extension
    else:
        return ''

def generate_random_list(length):
    # Generate a list of random characters of specified length
    random_list = random.choices(string.ascii_letters + string.digits, k=length)
    return ''.join(random_list)

def generate_filename(url):
    #filename = os.path.basename(url)
    #if filename == "file":
    #    filename = extract_directory(url)
    filename = extract_directory(url) + "-" + os.path.basename(url)
    if filename == "":
        filename = generate_random_list(10)
    if os.path.exists(directory_path + "/" + filename):
        filename = generate_random_list(10) + filename
    return directory_path + "/" + filename

def call_script_for_host(host, url):
    # Replace 'path_to_script' with the actual path to your script
    #subprocess.call(['python', 'path_to_script', host])
    print(f"Processing: [{host}] {url}")
    filename = generate_filename(url)

    if host == "mediafire.com":
        mediafire_dl.download(url, filename, quiet=False)

    if not bool(os.path.splitext(filename)[1]):
        print(f"Detected missing filename for {filename}")
        extension = generate_file_extension(filename)
        print(f"Renamed {filename} with extension \"{extension}\"")
        if extension:
            os.rename(filename, filename + extension)

    return True


def extract_host(url):
    parsed_url = urlparse(url)
    domain = tldextract.extract(parsed_url.netloc)
    return domain.registered_domain

def string_matches_file(string, file_path):
    if not os.path.exists(file_path):
        return False

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace and newline characters
            if line == string:
                return True
    return False

def append_line_to_file(line, file_path):
    with open(file_path, 'a+') as file:
        file.write(line + '\n')

if __name__ == "__main__":
    # Check if the directory argument is provided
    if len(sys.argv) < 2:
        print("Please provide a directory path as a command-line argument.")
        sys.exit(1)

    # Get the directory path from the command-line argument
    directory_path = sys.argv[1].removesuffix('/')

    # Check if the provided path is a valid directory
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    # Read URLs from stdin
    urls = sys.stdin.readlines()

    # Extract hosts from URLs and call script for each host
    for url in urls:
        if not string_matches_file(url, "downloaded.txt"):
            url = url.strip()  # Remove any leading/trailing whitespace or newlines
            host = extract_host(url)
            if call_script_for_host(host, url):
                append_line_to_file(url, "downloaded.txt")

