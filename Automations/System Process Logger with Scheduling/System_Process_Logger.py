import sys
import os
import time
import psutil
import schedule
import datetime

###################################################################################
#
# Function : createfolder
# Input    : folder name
# Output   : creates folder if it is not present
# Description : checks and creates log directory
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
# Output   : details of running processes
# Description : collects PID, name, user and memory usage
#
###################################################################################

def getprocessinfo():

    Processlist = []

    for proc in psutil.process_iter(['pid','name','username','memory_info']):

        try:

            info = proc.info

            pid = info['pid']
            pname = info['name']
            username = info['username']

            memory = info['memory_info']

            if memory is not None:
                memoryusage = round(memory.rss/(1024*1024),2)
            else:
                memoryusage = 0

            Processlist.append((pid,pname,username,memoryusage))

        except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            continue

    return Processlist


###################################################################################
#
# Function : createlogfile
# Input    : folder name
# Output   : creates timestamped log file
# Description : writes process information into log file
#
###################################################################################

def createlogfile(Directoryname):

    Processlist = getprocessinfo()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    Logfilename = "ProcessLog_%s.txt"%(timestamp)

    Logfilepath = os.path.join(Directoryname,Logfilename)

    fobj = open(Logfilepath,"w")

    fobj.write("="*70+"\n")
    fobj.write("System Process Logger\n")
    fobj.write("Date and Time : "+str(datetime.datetime.now())+"\n")
    fobj.write("="*70+"\n\n")

    fobj.write("{:<10} {:<25} {:<25} {:<15}\n".format(
        "PID","Process Name","Username","Memory(MB)"))

    fobj.write("-"*80+"\n")

    for process in Processlist: