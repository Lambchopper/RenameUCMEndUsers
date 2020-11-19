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
import getpass

#from suds.client import Client
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from lxml import etree
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

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

#AxlAPISchema = urljoin('file:', pathname2url(abspath('axlsqltoolkit/schema/11.5/AXLAPI.wsdl')))

# Allow insecure connections
#if hasattr(ssl, '_create_unverified_context'):
#    ssl._create_default_https_context = ssl._create_unverified_context

#Define a SOAP cliant
#CLIENT = Client(AxlAPISchema, location='https://%s:8443/axl/' % (strUCMIP), username=strUserID, password=strPassword)


#wsdl = 'file://C:/Development/Resources/axlsqltoolkit/schema/current/AXLAPI.wsdl'
wsdl = abspath('axlsqltoolkit/schema/11.5/AXLAPI.wsdl')
location = 'https://{host}:8443/axl/'.format(host=strUCMIP)
binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

session = Session()
session.verify = False
session.auth = HTTPBasicAuth(strUserID, strPassword)
transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
client = Client(wsdl=wsdl, transport=transport, plugins=[history])
service = client.create_service(binding, location)

def show_history():
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))

#Define a logging output
logfile = open(r'renamelocaluserlog.txt', 'a')
logfile.write(f'Begin new execution…\n')


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
          resp = service.updateUser(
               userid = OldUserName,
               newUserid = NewUserName
          )
     except:
          print("ERROR: Failed to connect to AXL terminating script")
          logfile.write(f'{OldUserName}\n')
          continue
    


#We are done and outta here!
exit()