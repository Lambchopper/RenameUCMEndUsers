#######################################
# renamelocalusers.py is used to automate the
# the renaming of Local UCM User accounts
# using AXL using a CSV file as input to
# automate the boring stuff for the Projects team.
# 
# Version 1.1
#######################################

#import necessary modules
from os.path import abspath
from urllib.parse import urljoin
from urllib.request import pathname2url
import ssl
from suds.client import Client
import getpass

#Collect the file with the list of  Users
print("\n")
print("="*56)
print("Enter the path and filename of the list of Users")
print("="*56)
strFile = input("File: ")
#Confirm file exists
try:
     with open(strFile) as f:
          listUserList = f.read().splitlines()
except:
     print("\n")
     print("File with List of UC Nodes not found.")
     print("Please check your file and try again.")
     exit()

#Collect UCM Pub IP or FQDN
print("\n")
print("="*56)
print("Enter the IP or FQDN of the CM Publisher for the target cluster")
print("="*56)
strUCMIP = input("IP or FQDN: ")

#Collect OS Admin Credentials
print("\n")
print("="*56)
print("Enter the CM Administrator credentials for this cluster")
print("="*56)
strUserID = input("User ID: ")
strPassword = getpass.getpass(prompt="Password: ")


#Collect path to the UCM AXL Schema
#The schema files are downloaded from UCM > Applications > Plugins > Cisco AXL Toolkit
print("\n")
print("="*56)
print("Connecting to Call Manager...")
print("="*56)
AxlAPISchema = urljoin('file:', pathname2url(abspath('axlsqltoolkit/schema/current/AXLAPI.wsdl')))

# Allow insecure connections
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

#Define a SOAP cliant
CLIENT = Client(AxlAPISchema, location='https://%s:8443/axl/' % (strUCMIP), username=strUserID, password=strPassword)


#Meat and Potatoes
print("\n")
print("="*56)
print("Modifying UserNames...")
print("="*56)
for user in listUserList:
     IndividualUser = user.split(",")
     OldUserName = IndividualUser[0]
     NewUserName = IndividualUser[1]
     print("{:40}{:40}".format("Changing: " + OldUserName, "To: " + NewUserName))

     try:
          resp = CLIENT.service.updateUser(
               userid = OldUserName,
               newUserid = NewUserName
          )
     except:
          print("ERROR: Failed to connect to AXL terminating script")
          exit()

#We are done and outta here!
exit()
