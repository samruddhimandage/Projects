###################################################################################
#
#  Program :     Duplicate File Finder and Deleter
#  Description : Finds duplicate files in a given directory using MD5
#                checksum and deletes duplicate files.
#  Input :       Directory name
#  Output :      Displays duplicate files and total deleted files.
#  Author :      Samruddhi Subhash Mandage
#
###################################################################################

import sys
import os
import hashlib

###################################################################################
#
#  Function :    calculatechecksum
#  Input :       File name
#  Description : Calculates the MD5 checksum of a given file.
#  Output :      Returns the checksum of the file.
#
###################################################################################

def calculatechecksum(filename):

    fobj = open(filename, "rb")

    hobj = hashlib.md5()

    Buffer = fobj.read(1024)

    while(len(Buffer) > 0):
        hobj.update(Buffer)
        Buffer = fobj.read(1024)

    fobj.close()

    return hobj.hexdigest()

###################################################################################
#
#  Function :    findduplicate
#  Input :       Directory name
#  Description : Finds duplicate files using their MD5 checksums.
#  Output :      Returns a dictionary containing duplicate files.
#
###################################################################################

def findduplicate(Directoryname):

    ret = False

    ret = os.path.exists(Directoryname)

    if ret == False:
        print("Path is invalid")
        return

    ret = os.path.isdir(Directoryname)

    if ret == False:
        print("No such directory")
        return

    duplicate = {}

    for foldername, subfolder, filename in os.walk(Directoryname):

        for fname in filename:

            fname = os.path.join(foldername, fname)

            checksum = calculatechecksum(fname)

            if checksum in duplicate:

                duplicate[checksum].append(fname)

            else:

                duplicate[checksum] = [fname]

    return duplicate

###################################################################################
#
#  Function :     deleteDuplicate
#  Input :        Directory name
#  Description :  Deletes duplicate files while keeping one original
#                 copy of each file.
#  Output :       Displays duplicate file names and total deleted files.
#
###################################################################################

def deleteDuplicate(directoryname):

    MyDict = findduplicate(directoryname)

    if MyDict is None:
        return

    result = list(filter(lambda x: len(x) > 1, MyDict.values()))

    count = 0
    total_deleted = 0

    for value in result:

        for subvalue in value:

            count = count + 1

            if count > 1:

                os.remove(subvalue)

                total_deleted = total_deleted + 1

                print("Duplicate found :", subvalue)

        count = 0

    print("Total deleted files :", total_deleted)

###################################################################################
#
#  Function :    main
#  Input :       Directory name
#  Description : Controls the execution of the program.
#
###################################################################################

def main():

    Border = "-" * 60

    print(Border)
    print("Welcome to Marvellous Duplicate File Finder")
    print(Border)

    if len(sys.argv) == 2:

        deleteDuplicate(sys.argv[1])

    else:

        print("Invalid input")
        print("Please execute the script as:")
        print("python Filename.py DirectoryName")

    print(Border)
    print("Thank you for using Marvellous Automation Script")
    print(Border)

###################################################################################
#
#  Starter of Automation Script
#
###################################################################################

if __name__ == "__main__":
    main()