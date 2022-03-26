import pymongo
import random
from employee import changePassword
from consign import loadConsignment
import string
from datetime import date


class Branch:
    def __init__(self, location, address, employees = [], numOfEmployees = 0, revenue = 0) -> None:
        self.location = location
        self.address = address
        self.employees = employees
        self.numOfEmployees = numOfEmployees
        self.revenue = revenue
        
    def convertToDictAndUpload(self) -> None:
        global settings
        id = settings.find_one({'_id':0})['BranchID']
        settings.update_one({'_id':0}, {'$set':{'BranchID':id+1}})
        branchDB.insert_one({'_id': id, 'Location':self.location, 'Address':self.address, 'Number Of Employees': self.numOfEmployees, 'Employees': self.employees, 'Revenue': self.revenue})

    def convertFromDict(dict):
        return Branch(dict['Location'], dict['Address'], dict['Employees'], dict['Number Of Employees'], dict['Revenue'])


def checkLogin(username, password):
    try:
        if username == "admin" and password == settings.find_one({'_id': 0})['managerPassword']:
            return 'SU'
        elif username == employeeDB.find_one({'email': username})['email'] and password == employeeDB.find_one({'email': username})['password']:
            return True
    except:
        return False

def generateRandomString():
    return ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randint(8, 12)))

def today():
    return str(date.today())

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
        return True
    except:
        return False

def nextEmptyTruckID(branch):
    return truckDB.find_one({'Branch': branch, 'Status': 'Empty'})['_id']

def loadUnloadedConsignments(branch):
    consignments = consignDB.find({'Branch': branch, 'Status': 'Unloaded'})
    for consignment in consignments:
        if loadConsignment(consignment['_id']):
            return

database = None
settings = None
employeeDB = None
branchDB = None
consignDB = None
truckDB = None
