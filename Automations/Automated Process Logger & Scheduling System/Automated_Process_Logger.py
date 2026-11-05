
import sys
import os
import time
import psutil
import schedule
import datetime

###################################################################################
#
# Function : createfolder
# Input    : Folder name
# Output   : Creates folder if not present
# Description : Creates directory for storing log files
#
###################################################################################

def createfolder(Directoryname):

    ret = os.path.exists(Directoryname)

    if ret == False:
        os.makedirs(Directoryname)

    return Directoryname


###################################################################################
#
# Function : getprocessinfo
# Input    : None
# Output   : Running process information
# Description : Collects details of running processes
#
###################################################################################

def getprocessinfo():

    Processlist = []

    for proc in psutil.process_iter(['pid','name','username','status']):

        try:

            info = proc.info

            pid = info['pid']
            pname = info['name']
            username = info['username']
            status = info['status']

            Processlist.append((pid,pname,username,status))

        except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            continue

    return Processlist


###################################################################################
#
# Function : createlogfile
# Input    : Folder name
# Output   : Creates timestamped log file
# Description : Writes process details into log file
#
###################################################################################

def createlogfile(Directoryname):

    Processlist = getprocessinfo()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    Logfilename = "ProcessLog_%s.txt"%(timestamp)

    Logfilepath = os.path.join(Directoryname,Logfilename)

    fobj = open(Logfilepath,"w")

    fobj.write("="*70+"\n")
    fobj.write("Automated Process Logger\n")
    fobj.write("Date and Time : "+str(datetime.datetime.now())+"\n")
    fobj.write("="*70+"\n\n")

    fobj.write("{:<10} {:<30} {:<25} {:<15}\n".format(
        "PID","Process Name","Username","Status"))

    fobj.write("-"*80+"\n")

    for process in Processlist:

        pid,pname,username,status = process

        fobj.write("{:<10} {:<30} {:<25} {:<15}\n".format(
            str(pid),str(pname),str(username),str(status)))

    fobj.write("\n")
    fobj.write("Total Processes Logged : "+str(len(Processlist))+"\n")
    fobj.write("="*70+"\n")

    fobj.close()

    print("\nLog file created successfully")
    print("Log file name :",Logfilepath)
    print("Total processes logged :",len(Processlist))


###################################################################################
#
# Function : processlogger
# Input    : Folder name
# Description : Performs process scanning and log generation
#
###################################################################################

def processlogger(Directoryname):

    print("\n")
    print("-"*60)
    print("Automated Process Logger")
    print("-"*60)

    createlogfile(Directoryname)


###################################################################################
#
# Function : main
# Description : Accepts folder name and time interval
#
###################################################################################

def main():

    Border = "-"*60

    print(Border)
    print("Welcome to Automated Process Logger")
    print(Border)

    if(len(sys.argv)==2):

        if(sys.argv[1]=="--h" or sys.argv[1]=="--H"):

            print("This script automatically generates system process logs")
            print("Please check --u flag for usage")

        elif(sys.argv[1]=="--u" or sys.argv[1]=="--U"):

            print("Please execute the script as")
            print("python Automated_Process_Logger.py FolderName IntervalInMinutes")

        else:

            print("Invalid command line arguments")

    elif(len(sys.argv)==3):

        Directoryname = sys.argv[1]

        try:

            Interval = int(sys.argv[2])

        except ValueError:

            print("Please enter valid time interval")
            return

        if Interval <= 0:

            print("Time interval should be greater than zero")
            return

        createfolder(Directoryname)

        print("\nLog folder :",Directoryname)
        print("Logging interval :",Interval,"minutes")

        # Generate first log immediately
        processlogger(Directoryname)

        # Schedule automatic log generation
        schedule.every(Interval).minutes.do(processlogger,Directoryname)

        print("\nAutomated process logging started...")
        print("Press CTRL+C to stop logging")

        try:

            while(True):

                schedule.run_pending()

                time.sleep(1)

        except KeyboardInterrupt:

            print("\nProcess logging stopped by user")

    else:

        print("Invalid number of arguments")
        print("Use --h for help and --u for usage")

    print(Border)
    print("Thank you for using Automated Process Logger")
    print(Border)


###################################################################################

if __name__=="__main__":
    main()
