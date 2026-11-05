Platform Surveillance System
Description
Platform Surveillance System is a Python command-line utility that monitors a computer's system performance and running processes. It collects CPU usage, RAM utilization, disk statistics, network counters, and process information using the psutil library. Reports are displayed on the terminal and appended to a log file at regular intervals.
Features
- Monitors CPU utilization.
- Reports RAM usage, total memory, and available memory.
- Reports disk usage, total disk space, and free space.
- Collects network bytes and packet counters.
- Lists running processes with PID, name, user, and status.
- Displays a report in the terminal.
- Appends periodic reports to System_Monitoring.log.
- Runs continuously at a user-defined interval.
Technologies Used
- Python
- psutil
- schedule
- os, sys, time, datetime (Python standard library)
Requirements
- Python 3.8 or later
- psutil
- schedule
Installation
Open a terminal in the project directory and run:
pip install -r req.txt
Usage
Start monitoring with an interval in minutes:
python Platform_Surveillance.py 1
This example performs an initial report immediately, then generates another report every 1 minute.

Show help:
python Platform_Surveillance.py --h
Show usage:
python Platform_Surveillance.py --u
Stop monitoring with Ctrl+C.
Output
The program displays CPU, RAM, disk, network, and process information in the terminal. It also appends each report to:
System_Monitoring.log
The log file is created in the current working directory if it does not already exist.
Project Structure
Platform_Surveillance/
├── Platform_Surveillance.py
├── README.md
└── req.txt
Notes
- Network values are cumulative counters reported by the operating system since boot; they are not per-interval network speeds.
- Process details may be unavailable for protected or system processes. Such access errors are skipped.
- Disk usage is reported for the root drive or filesystem. On Windows, this is the drive containing the root path.
- This project is intended for educational system-monitoring and administration practice.