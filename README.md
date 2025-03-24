# File encryption with Python

Generate a zip file and encrypt it with a random password. Tested on Linux, should also work on Mac.

## Usage

Run the following command to execute the script:

```bash
python3 encrypt.py -f <file_to_encrypt> -l <password_length>
```

Replace <file_to_encrypt> with the path to the file you want to encrypt and <password_length> with the desired password length (default is 12).

If no input file is given and tk is installed, a file selecter allows you to pick a file.
Then, a zip file is generated with a random password. The password is showed in the terminal and automatically copied to the clipboard.
NB: multiple file selection is currently not supported.

You can omit python3 if the file has the right permissions.

```bash
chmod +x encrypt.py
```

