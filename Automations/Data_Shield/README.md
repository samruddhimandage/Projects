
# Data Shield – Automated Backup & File Monitoring System

## Description

Data Shield is a Python-based automated backup and file monitoring system. It helps users securely manage and synchronize important data directories.

The system uses MD5 checksum comparison to detect newly added and modified files. It automatically copies updated files to the backup directory and creates ZIP archives for backup management.

## Features

- Automatic file backup.
- Detects newly added files.
- Detects modified files using MD5 checksum.
- Skips unchanged files.
- Automatic periodic backup using schedule module.
- Creates timestamp-based ZIP archives.
- Command-line interface for easy execution.
- Displays backup status and reports.

## Technologies Used

- Python
- OS Module
- hashlib
- shutil
- schedule
- zipfile
- datetime
- sys

## Installation

Install the required Python library using:

```bash
pip install -r req.txt
```

## How to Run

Execute the program using the following command:

```bash
python Data_Shield.py Source Backup 2
```

Here:

- Source: Directory containing original files.
- Backup: Directory where backup files are stored.
- 2: Backup interval in minutes.

## Command Line Arguments

Display help:

```bash
python Data_Shield.py --h
```

Display usage:

```bash
python Data_Shield.py --u
```

## Working

1. The program scans the source directory.
2. It calculates the MD5 checksum of each file.
3. It compares the checksum with the backup file.
4. New files are copied to the backup directory.
5. Modified files are updated in the backup directory.
6. Unchanged files are skipped.
7. A ZIP archive is created after every backup operation.
8. The schedule module executes the backup periodically.

## Output

The program displays the number of new, modified and unchanged files along with the backup archive location.

## Note

The program does not automatically delete files from the backup directory when they are deleted from the source directory.

This project is developed for educational and practical purposes.
