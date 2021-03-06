import pymongo
import random
from employee import changePassword
import consign
import string
from datetime import date, datetime
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from mail import sendMail

geolocator = Nominatim(user_agent='TCC')

def distance(city1, city2):             # returns distance between two cities in km
    location1 = geolocator.geocode(city1)
    location2 = geolocator.geocode(city2)
    return geodesic((location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).km

def closestBranch(address):         # returns the closest branch to the address
    city = address.split(', ')[-1]
    minDistance = 100000
    closestBranch = ''
    for branch in list(branchDB.find()):
        if distance(city, branch['Location']) < minDistance:
            minDistance = distance(city, branch['Location'])
            closestBranch = branch['Location']
    return closestBranch


class Branch:
    def __init__(self, location, address) -> None:      # constructor
        self.location = location
        self.address = address
        
    def convertToDictAndUpload(self) -> None:           # convert to dictionary and upload to database
        global settings
        id = settings.find_one({'_id':0})['BranchID']
        settings.update_one({'_id':0}, {'$set':{'BranchID':id+1}})
        branchDB.insert_one({
            '_id': id, 
            'Location':self.location, 
            'Address':self.address, 
            'Number Of Employees': 0, 
            'Employees': [], 
            'Revenue': 0,
            'Average Waiting Time for Consignments': 0.00,
            'Number of Consignments Delivered': 0})

    def convertFromDict(dict):
        return Branch(dict['Location'], dict['Address'])


def checkLogin(username, password):         # returns true if username and password are correct for employee, 'SU' if the manager, else False
    try:
        if username == "admin" and password == settings.find_one({'_id': 0})['managerPassword']:
            return 'SU'
        else:
            employee = employeeDB.find_one({'Email': username})
            if employee is not None and employee['Password'] == password:
                global employeeUser
                employeeUser = employee
                return True
            return False
    except:
        return False

def stringToDateTime(string):           # converts string to datetime
    return datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')

def generateRandomString():         # generates a random string of length 8 - 11
    return ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randint(8, 12)))

def deltaTimeToHours(s1, s2):           # returns the difference between two datetime objects in hours  
    d = s2 - s1
    return (d.days * 24 + d.seconds / 3600)

def today():                     # returns today's date in string format
    return str(date.today())

def now():                      # returns current time in string format
    return str(datetime.now())

def setupDB():                  # sets up the database
    global database, employeeDB, settings, branchDB, truckDB, consignDB
    cluster = pymongo.MongoClient("mongodb://selabproject:selabproject@se-shard-00-00.hl6lf.mongodb.net:27017,se-shard-00-01.hl6lf.mongodb.net:27017,se-shard-00-02.hl6lf.mongodb.net:27017/TCC?ssl=true&replicaSet=atlas-ee0z3v-shard-0&authSource=admin&retryWrites=true&w=majority")
    database = cluster['TCC']
    settings = database['Settings']
    employeeDB = database['Employee']
    branchDB = database['Branch']
    consignDB = database['Consignment']
    truckDB = database['Truck']

def mailPassword(email):            # sends reset password to the email
    try:
        # mail password
        password = generateRandomString()
        changePassword(email, password)
        sendMail(email, False, password)
        return True
    except:
        return False

def nextAvailableTruck(branch, consign):            # returns the next available truck for the consignment
    nearestBranch = consign['Destination']
    truck = truckDB.find_one({'Location': branch, 'Next Destination': nearestBranch, 'Status': 'Available'}) 
    if truck is not None:
        return truck
    truck = truckDB.find_one({'Location': branch, 'Next Destination': 'NA', 'Status': 'Available'}) 
    return truck

def loadUnloadedConsignments(branch):               # loads all unloaded consignments from the database inside given branch
    consignments = list(consignDB.find({'At Branch': branch, 'Status': 'Unloaded'}))
    if len(consignments) == 0:
        return
    curTruck = nextAvailableTruck(branch, consignments[0])
    for i in range(len(consignments)):
        if consign.loadConsignment(consignments[i]['_id'], curTruck):
            curTruck = nextAvailableTruck(branch, consignments[i])
        if curTruck is None:
            return

database = None
settings = None
employeeDB = None
branchDB = None
consignDB = None
truckDB = None
employeeUser = None
Rate = 50