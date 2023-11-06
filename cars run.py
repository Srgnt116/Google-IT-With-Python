#! /usr/bin/env python3

import os
import requests

def uploadFeedback():
    #Creates a list of all files in the current working directory
    os.chdir(fileLoca)
    print(os.getcwd())
    fbFiles = os.listdir(fileLoca)
    print("The following files will be uploaded: {}".format(fbFiles))
    proceedORnaw = input("Would you like to proceed? y or n:   ")
    if proceedORnaw == "y":
        fbList = []
        count = 0
        for root, dirs, files in os.walk(fileLoca):
            for filename in files:
                with open(filename) as file:
                    count += 1
                    info = file.read().split("\n")
                    fbDic = {'title':info[0], 'name':info[1], 'date':info[2], 'feedback':info[3]}
#                   proceedORnaw = input("Would you like to view the data prior to transmission? y or n:   ")
#                   if proceedORnaw == "y":
#                       print(fbDic)
                    fbList.append(fbDic)
                    fbFormSent = requests.post(websiteURL, json=fbDic)
                    if fbFormSent.status_code == 201:
                        print("Successfully posted feedback form no. {}".format(count))
                    else:
                        print("Error encountered, status code recieved: {}".format(fbFormSent.status_code))
        print("Task Complete.  Posted {} feedback forms to {}".format(count, websiteURL) )
# The coding below may help identify issues with incorrect information being posted and
# is a list of the dictionaries posted.  It may be better to have it print only the dictionary
# you had a problem with earlier in the coding
#        print("Would you like to view the information submitted?")
#        proceedORnaw = input("y or n:   ")
#        if proceedORnaw == "y":
#            print(fbList)

print("Enter website URL feedback forms are to be uploaded to")
print("Be sure to include 'http://' and to include a '/' at the end of the address")
websiteURL = input("Full website address:   ")
print("Enter the location of the feedback forms to be uploaded")
print("This should start with a '/' and end with a '/'")
fileLoca = input("File Location:   ")
print("Feedback forms in {} will be uploaded to {}".format(fileLoca, websiteURL))
print("Ensure this information is correct! Any issues will cause unexpected results")
proceedORnaw = input("Would you like to proceed? y or n:   ")
if proceedORnaw == "y":
    uploadFeedback()
