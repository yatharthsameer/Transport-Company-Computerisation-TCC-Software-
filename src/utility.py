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

def distance(city1, city2):
    location1 = geolocator.geocode(city1)
    location2 = geolocator.geocode(city2)
    return geodesic((location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).km

def closestBranch(address):
    city = address.split(', ')[-1]
    minDistance = 100000
    closestBranch = ''
    for branch in branchDB.find():
        if distance(city, branch['Location']) < minDistance:
            minDistance = distance(city, branch['Location'])
            closestBranch = branch['Location']
    return closestBranch


class Branch:
    def __init__(self, location, address) -> None:
        self.location = location
        self.address = address
        
    def convertToDictAndUpload(self) -> None:
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
            'Avg. Waiting Time for Consignments': 0,
            'No. of Consignments Delivered': 0})

    def convertFromDict(dict):
        return Branch(dict['Location'], dict['Address'], dict['Employees'], dict['Number Of Employees'], dict['Revenue'])


def checkLogin(username, password):
    try:
        if username == "admin" and password == settings.find_one({'_id': 0})['managerPassword']:
            return 'SU'
        else:
            employee = employeeDB.find_one({'email': username})
            if employee is not None and employee['Password'] == password:
                global employeeUser
                employeeUser = employee
                return True
    except:
        return False

def stringToDateTime(string):
    return datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')

def generateRandomString():
    return ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randint(8, 12)))

def deltaTimeToHours(s1, s2):
    d = s2 - s1
    return (d.days * 24 + d.seconds / 3600)

def today():
    return str(date.today())

def now():
    return str(datetime.now())

def setupDB():
    global database, employeeDB, settings, branchDB, truckDB, consignDB
    cluster = pymongo.MongoClient("mongodb://selabproject:selabproject@se-shard-00-00.hl6lf.mongodb.net:27017,se-shard-00-01.hl6lf.mongodb.net:27017,se-shard-00-02.hl6lf.mongodb.net:27017/TCC?ssl=true&replicaSet=atlas-ee0z3v-shard-0&authSource=admin&retryWrites=true&w=majority")
    database = cluster['TCC']
    settings = database['Settings']
    employeeDB = database['Employee']
    branchDB = database['Branch']
    consignDB = database['Consignment']
    truckDB = database['Truck']

def mailPassword(email):
    try:
        # mail password
        password = generateRandomString()
        changePassword(email, password)
        sendMail(email, False, password)
        return True
    except:
        return False

def nextAvailableTruck(branch, consign):
    nearestBranch = consign['Destination']
    truck = truckDB.find_one({'Location': branch, 'Next Destination': nearestBranch, 'Status': 'Available'}) 
    if truck is not None:
        return truck
    truck = truckDB.find_one({'Location': branch, 'Next Destination': 'NA', 'Status': 'Available'}) 
    return truck

def loadUnloadedConsignments(branch):
    consignments = consignDB.find({'At Branch': branch, 'Status': 'Unloaded'})
    curTruck = nextAvailableTruck(branch)
    for consignment in consignments:
        if curTruck is None:
            return
        if consign.loadConsignment(consignment['_id'], curTruck):
            curTruck = nextAvailableTruck(branch, consignment)

database = None
settings = None
employeeDB = None
branchDB = None
consignDB = None
truckDB = None
employeeUser = None