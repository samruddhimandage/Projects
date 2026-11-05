
# Duplicate File Finder and Deleter

## Description

Duplicate File Finder and Deleter is a Python-based utility designed to identify and remove duplicate files from a specified directory.

The program uses MD5 checksum comparison through the hashlib module to identify files having identical content. It keeps one original copy and deletes the remaining duplicate files.

## Features

- Scans files inside a specified directory.
- Supports directory traversal using os.walk().
- Calculates MD5 checksum of files.
- Identifies duplicate files based on checksum comparison.
- Preserves one original copy of each duplicate group.
- Deletes additional duplicate files automatically.
- Displays duplicate file names.
- Displays the total number of deleted files.
- Validates the given directory path.

## Technologies Used

- Python
- hashlib
- os
- sys

## Requirements

- Python 3.x
- No external Python libraries are required.

## How to Run

Execute the program using the following command:

```bash
python directory_checksum_delete_final.py FolderName
```

Example:

```bash
python directory_checksum_delete_final.py Data
```

Here:

- Data is the directory in which duplicate files will be searched.
- The program scans the directory and its subdirectories.
- Duplicate files are identified and deleted automatically.

## Working

1. Accepts a directory name through command-line arguments.
2. Checks whether the specified directory exists.
3. Scans all files using os.walk().
4. Calculates the MD5 checksum of every file.
5. Stores file paths according to their checksums.
6. Identifies files having matching checksums.
7. Keeps the first file as the original copy.
8. Deletes the remaining duplicate files.
9. Displays the total number of deleted files.

## Output

The program displays duplicate file information and the total number of deleted files.

Example:

```text
------------------------------------------------------------
Welcome to Marvellous Duplicate File Finder
------------------------------------------------------------

Duplicate found : Data/file2.txt
Duplicate found : Data/file3.txt

Total deleted files : 2

------------------------------------------------------------
Thank you for using Marvellous Automation Script
------------------------------------------------------------
```

## Project Structure

```text
Duplicate_File_Finder/
│
├── directory_checksum_delete_final.py
├── README.md
└── req.txt
```

## Important Note

- The program permanently deletes duplicate files.
- One original copy is preserved for each group of files having matching MD5 checksums.
- MD5 checksum comparison is intended for basic duplicate detection and is not a security guarantee.
- Review important files before running the deletion operation.

## Conclusion

This project demonstrates file handling, directory traversal, checksum calculation, duplicate detection and file deletion using Python.
