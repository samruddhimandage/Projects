
# System Process Logger with Scheduling

## Description

System Process Logger is a Python automation project that periodically records details of running processes. It collects process ID (PID), process name, username and memory usage using the psutil library.

Each execution generates a separate log file with a timestamped filename for easy tracking.

The schedule library is used to execute the logging task automatically at a user-defined interval.

## Features

- Scans currently running system processes.
- Records Process ID (PID).
- Records process name.
- Records username.
- Monitors memory usage in MB.
- Creates timestamped log files.
- Allows custom log folder name.
- Allows custom logging interval.
- Performs automatic periodic logging.
- Handles inaccessible and terminated processes.

## Technologies Used

- Python
- psutil
- schedule
- os
- sys
- time
- datetime

## Installation

Install the required libraries using:

```bash
pip install -r req.txt
```

## How to Run

Execute the program using:

```bash
python System_Process_Logger.py Logs 1
```

Here:

- Logs: Folder name where log files will be stored.
- 1: Logging interval in minutes.

The first log file is generated immediately. After that, a new log file is generated every minute.

## Command Line Arguments

Display help:

```bash
python System_Process_Logger.py --h
```

Display usage:

```bash
python System_Process_Logger.py --u
```

## Output

The program creates timestamped log files inside the specified folder.

Example:

```text
Logs/
    ProcessLog_20261105_172300.txt
    ProcessLog_20261105_172400.txt
    ProcessLog_20261105_172500.txt
```

Each log file contains:

- Date and time
- Process ID
- Process name
- Username
- Memory usage
- Total number of processes

## Project Structure

```text
System_Process_Logger/
│
├── System_Process_Logger.py
├── README.md
└── req.txt
```

## Note

Some system processes may be skipped if access is denied or if the process terminates during scanning.

This project is developed for educational and Python automation practical purposes.
