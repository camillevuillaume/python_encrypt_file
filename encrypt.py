#!/usr/bin/env python3

import random
import string
import argparse
import subprocess
import os
import platform

def copy_to_clipboard(password):
    """
    Copies the given password to the clipboard.

    Supports macOS, Linux (Wayland and X11), and Windows. 
    Prints a message if the clipboard utility is not found.

    Args:
        password (str): The password to copy to the clipboard.
    """    
    # Detect the operating system
    current_os = platform.system()
    
    try:
        if current_os == "Darwin":  # macOS
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(input=password.encode('utf-8'))
            print('Password copied to clipboard.')
        elif current_os == "Linux":
            # Check if wl-copy is available for Wayland
            if os.environ.get('WAYLAND_DISPLAY'):
                process = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE)
                process.communicate(input=password.encode('utf-8'))
                print('Password copied to clipboard using wl-copy (Wayland).')
            else:
                # Fallback to xclip for X11
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                process.communicate(input=password.encode('utf-8'))
                print('Password copied to clipboard using xclip (X11).')
        elif current_os == "Windows":
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
            process.communicate(input=password.encode('utf-8'))
            print('Password copied to clipboard.')
        else:
            print(f"Clipboard copy not supported on {current_os}.")
    except FileNotFoundError:
        print(f"Clipboard utility not found on {current_os}. Please install the required tool (e.g., xclip for Linux).")

def select_files():
    """
    Open a file dialog to select files.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog

        # Hide main root window
        root = tk.Tk()
        root.withdraw()  # This withdraws the root window so it doesn't appear

        # Open file dialog allowing multiple file selections
        file_paths = filedialog.askopenfilenames(
            title="Select files",
            filetypes=(("All files", "*.*"),)
        )
        return file_paths
    except ImportError:
        print("tkinter is not available on this system. Please install it to use the file selection feature.")
        return []
    
def generate_password(length=12):
    """
    Generate a random password with the specified length.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def encrypt_file_with_zip(input_file, password, archive_name):
    """
    Encrypt a file using the zip command with a password.
    """
    print(input_file)
    # Use the subprocess module to call the zip command
    zip_command = ['zip', '-e', '-P', password, f'{archive_name}.zip', input_file]
    subprocess.run(zip_command, check=True)

def main():
    parser = argparse.ArgumentParser(description='Generate a random password, encrypt a file, and copy the password to clipboard.')
    parser.add_argument('-l', '--length', type=int, default=12, help='Length of the password')
    parser.add_argument('-f', '--file', type=str, help='File to encrypt')

    args = parser.parse_args()
    if(not args.file):
        selected_files = select_files()
        if not selected_files:
            parser.print_help()
            print("No files selected. Exiting.")
            return
        files_to_encrypt = ''
        for file in selected_files:
            file_dir, file_name = os.path.split(file)
            files_to_encrypt += file_name
    else:
        file_dir, file_name = os.path.split(args.file)
        if(file_dir == ''):
            file_dir = os.getcwd()
        files_to_encrypt = file_name

    # Save the original working directory
    original_dir = os.getcwd()

    try:
         # Change to the directory containing the file
        os.chdir(file_dir)
        password = generate_password(args.length)

        # Encrypt the file using the generated password
        encrypt_file_with_zip(files_to_encrypt, password, file_name)

        print(f'File "{files_to_encrypt}" encrypted and saved as "{files_to_encrypt}.zip" with password {password}.')

        # Copy to clipboard
        copy_to_clipboard(password)

    except subprocess.CalledProcessError as e:
        print(f'An error occurred while encrypting the file: {e}')

    finally:
        # Change back to the original working directory
        os.chdir(original_dir)

if __name__ == "__main__":
    main()