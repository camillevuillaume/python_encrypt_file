#!/usr/bin/env python3

import random
import string
import argparse
import subprocess
import tkinter as tk
from tkinter import filedialog

def select_files():
    # Hide main root window
    root = tk.Tk()
    root.withdraw()  # This withdraws the root window so it doesn't appear

    # Open file dialog allowing multiple file selections
    file_paths = filedialog.askopenfilenames(
        title="Select files",
        filetypes=(("All files", "*.*"),)
    )
    return file_paths

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def encrypt_file_with_zip(input_file, password):
    print(input_file)
    # Use the subprocess module to call the zip command
    zip_command = ['zip', '-e', '-P', password, f'{input_file}.zip', input_file]
    subprocess.run(zip_command, check=True)

def main():
    parser = argparse.ArgumentParser(description='Generate a random password, encrypt a file, and copy the password to clipboard.')
    parser.add_argument('-l', '--length', type=int, default=12, help='Length of the password')
    parser.add_argument('-f', '--file', type=str, help='File to encrypt')

    args = parser.parse_args()
    if(not args.file):
        files_to_encrypt = ' '.join(select_files())
    else:
        files_to_encrypt = args.file

    password = generate_password(args.length)

    try:
        # Encrypt the file using the generated password
        encrypt_file_with_zip(files_to_encrypt, password)

        print(f'File "{args.file}" encrypted and saved as "{args.file}.zip" with password {password}.')
        # Use subprocess to run pbcopy and pipe the password
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(input=password.encode('utf-8'))
        print('Password copied to clipboard.')

    except subprocess.CalledProcessError as e:
        print(f'An error occurred while encrypting the file: {e}')

if __name__ == "__main__":
    main()