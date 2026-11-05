
# Automated Process Logger & Scheduling System

## Description

Automated Process Logger is a Python-based automation project designed to periodically generate and manage system process log files.

It collects information about running processes using the psutil library and stores the details in separate timestamped log files.

The schedule library is used to automate log generation at user-defined intervals.

## Features

- Automatic system process scanning.
- Collects process ID (PID).
- Collects process name.
- Collects username.
- Collects process status.
- Creates timestamp-based log files.
- Supports custom folder name.
- Supports custom logging interval.
- Automatic periodic log generation.
- Maintains separate log files for every execution.
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
python Automated_Process_Logger.py Logs 1
```

Here:

- Logs: Folder name where log files will be stored.
- 1: Logging interval in minutes.

The program generates the first log immediately and then automatically generates new log files every minute.

## Command Line Arguments

Display help:

```bash
python Automated_Process_Logger.py --h
```

Display usage:

```bash
python Automated_Process_Logger.py --u
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
- Process status
- Total number of processes logged

## Project Structure

```text
Automated_Process_Logger/
│
├── Automated_Process_Logger.py
├── README.md
└── req.txt
```

## Note

Some system processes may be skipped if access is denied or if a process terminates during scanning.

This project is developed for educational and Python automation practical purposes.
