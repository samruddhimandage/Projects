
# Automated Email Notification & Scheduling System

## Description

Automated Email Notification & Scheduling System is a Python-based automation project designed to send emails automatically at predefined time intervals.

The system uses SMTP communication with Gmail to send emails securely. It uses the smtplib module for email transmission and EmailMessage for creating email messages.

The schedule library is used to automate email delivery at regular intervals without manual intervention.

## Features

- Automatic email sending.
- SMTP-based email communication.
- Secure Gmail SMTP connection using SSL.
- Email authentication using sender credentials.
- Custom sender email address.
- Custom receiver email address.
- Custom email subject.
- Custom email message body.
- Periodic email scheduling.
- Automatic email delivery without manual intervention.

## Technologies Used

- Python
- smtplib
- EmailMessage
- schedule
- time
- datetime

## Requirements

- Python 3.x
- schedule library
- Gmail account
- Gmail App Password

## Installation

Install the required Python library using:

```bash
pip install -r req.txt
```

## Gmail Configuration

To send emails using Gmail SMTP:

1. Enable 2-Step Verification in your Google account.
2. Generate a Gmail App Password.
3. Use the generated App Password in the Python program.
4. Enter the sender and receiver email addresses.

Note: Do not use your regular Gmail account password. Use an App Password.

## How to Run

Execute the program using:

```bash
python Automated_Email.py
```

The program starts the email scheduler and automatically sends emails at the configured interval.

## Email Configuration

The following details can be customized in the Python program:

- Sender Email Address
- Gmail App Password
- Receiver Email Address
- Email Subject
- Email Message Body

## Scheduling

The schedule library is configured to send an email every 10 seconds.

The scheduler continuously checks pending tasks and sends emails automatically at the specified interval.

To change the interval, modify the following statement in the Python program:

```python
schedule.every(10).seconds.do(
    send_email,
    sender_email,
    app_password,
    receiver_email,
    subject,
    body
)
```

## Working

1. The program imports the required Python modules.
2. Email details are configured.
3. EmailMessage creates the email message.
4. SMTP_SSL establishes a secure connection with Gmail.
5. The sender is authenticated using the Gmail App Password.
6. The email is sent to the receiver.
7. The schedule library executes the email task periodically.
8. The program continues running until manually stopped.

## Output

```text
Email scheduler started...
Mail sent successfully
Mail sent successfully
Mail sent successfully
```

## Project Structure

```text
Automated_Email/
│
├── Automated_Email.py
├── README.md
└── req.txt
```

## Important Notes

- An active internet connection is required.
- Gmail SMTP uses smtp.gmail.com on port 465 with SSL.
- A valid Gmail App Password is required.
- Keep your App Password private.
- The program continues running until stopped using CTRL+C.
- The email is sent every 10 seconds as configured in the script.

## Conclusion

This project demonstrates email automation, secure SMTP communication, email authentication and periodic task scheduling using Python.
