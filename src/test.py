import bill, consign, db, employee, mail, manager, truck, utility
import datetime

print('utility.setupDB')
try:    
    utility.setupDB()
    print('PASS')
except:
    print('FAIL')

print('utility.distance(): cities non existent')
try:    
    utility.distance('addddd', 'addddd')
    print('PASS')
except: 
    print('FAIL')

print('utility.distance(): cities exist')
try:    
    utility.distance('Indore', 'Bhopal')
    print('PASS')
except:
    print('FAIL')

print('utility.checkLogin(): both username and password are correct')
try:     
    utility.checkLogin('admin', 'admin')
    print('PASS')
except: 
    print('FAIL')

print('utility.checkLogin(): do not match')
try:    
    utility.checkLogin('ad', 'ad')
    print('PASS')
except:
    print('FAIL')

print('utility.stringToDateTime(): non string data type')
try:    
    utility.stringToDateTime(3, 5)
    print('PASS')
except:
    print('FAIL')

print('utility.stringToDateTime(): string but not formatted')
try:    
    utility.stringToDateTime('3/5/20')
    print('PASS')
except: 
    print('FAIL')


print('utility.stringToDateTime(): well formatted string ')
try:    
    utility.stringToDateTime(utility.now())
    print('PASS')
except: 
    print('FAIL')

print('utility.generateRandomString()')
try:    
    utility.generateRandomString()
    print('PASS')
except: 
    print('FAIL')

print('utility.deltaTimeToHours(): arguments are not datetime objects')
try:    
    utility.deltaTimeToHours(34, 34)
    print('PASS')
except:
    print('FAIL')

print('utility.deltaTimeToHours(): arguments are datetime objects')
try:    
    utility.deltaTimeToHours(datetime.datetime.now(), datetime.datetime.now())
    print('PASS')
except: 
    print('FAIL')

print('utility.today()')
try:    
    print(utility.today())
    print('PASS')
except:
    print('FAIL')

print('utility.now()')
try:     
    print(utility.now())
    print('PASS')
except: 
    print('FAIL')

print('utility.mailPassword(): wrong mail id')
try:    
    utility.mailPassword('assign')
    print('PASS')
except:
    print('FAIL')

print('utility.mailPassword(): existing email id')
try:    
    utility.mailPassword('atulyaankitsharma@gmail.com')
    print('PASS')
except:
    print('FAIL')

branch = None

print('utility.Branch()')
try:    
    branch = utility.Branch('Indore', 'address, Indore')
    print('PASS')
except:
    print('FAIL')

print('branch.convertToDictAndUpload()')
try:        
    branch.convertToDictAndUpload()
    print('PASS')
except:
    print('FAIL')

print('branch.convertFromDict(): incorrect dictionary format')
try:    
    utility.Branch.convertFromDict(utility.branchDB.find_one({'_id':0}))
    print('PASS')
except:
    print('FAIL')

print('branch.convertFromDict(): correct dictionary format')
try:    
    utility.Branch.convertFromDict({'Location': 'loc', 'Address': 'ad'})
    print('PASS')
except:
    print('FAIL')

print('utility.closestBranch(): address not formatted')
try:    
    utility.closestBranch('Indore')
    print('PASS')
except:
    print('FAIL')

print('utility.closestBranch(): address formatted')
try:     
    utility.closestBranch('something, Indore')
    print('PASS')
except: 
    print('FAIL')


print('employee.changePassword()')
try:    
    employee.changePassword('aa', 'password')
    print('PASS')
except:
    print('FAIL')

employeeObj = None

print('employee.Employee()')
try:    
    employeeObj = employee.Employee('name', 123, 'mail', 'add', 'Indore')
    print('PASS')
except: 
    print('FAIL')

truckObj = None

print('truck.Truck()')
try:    
    truckObj = truck.Truck('plate', 'Indore', 'driver', 123)
    print('PASS')
except:
    print('FAIL')

print('convertToDictAndUpload()')
try:    
    truckObj.convertToDictAndUpload()
    print('PASS')
except:
    print('FAIL')

print('consign.Consign()')
try:    
    consignObj = consign.Consign('a', 'a', 12, 'a', 'a', 'a, Indore', 510, 'Indore', 'a')
    print('PASS')
except:
    print('FAIL')

print('consign.convertToDictAndUpload()')
try:
    consignObj.convertToDictAndUpload()
    print('PASS')
except:
    print('FAIL')

print('mail.sendMail(): wrong mail id')
try:    
    mail.sendMail('mail', False, 'pass')
    print('PASS')
except:
    print('FAIL')

print('mail.sendMail(): existing mail id')
try:    
    mail.sendMail('atulyaankitsharma@gmail.com', False, 'pass')
    print('PASS')
except:
    print('FAIL')

print('manager.branchQuery(): existing branch name')
try:    
    manager.branchQuery('Indore')
    print('PASS')
except:
    print('FAIL')

print('manager.branchQuery(): non existing branch name')
try:    
    manager.branchQuery('branch')
    print('PASS')
except:
    print('FAIL')

print('manager.truckQuery(): existing truck')
try:    
    manager.truckQuery(1, 'plate')
    print('PASS')
except:
    print('FAIL')

print('manager.truckQuery(): non existing truck')
try:    
    manager.truckQuery(2, 'plate')
    print('PASS')
except:
    print('FAIL')

print(' manager.employeeQuery(): existing employee')
try:    
    manager.employeeQuery(1, 'name')
    print('PASS')
except:
    print('FAIL')

print(' manager.employeeQuery(): non existing employee')
try:    
    manager.employeeQuery(2, 'name')
    print('PASS')
except:
    print('FAIL')

print('manager.consignmentQuery(): existing consignment id')
try:    
    manager.consignmentQuery(1, '', '')
    print('PASS')
except:
    print('FAIL')

print('manager.consignmentQuery(): non existing consignment id')
try:    
    manager.consignmentQuery(2, '', '')
    print('PASS')
except:
    print('FAIL')

print('manager.queryConsignmentsHeadedToSameBranch()')
try:    
    manager.queryConsignmentsHeadedToSameBranch('Indore')
    manager.queryConsignmentsHeadedToSameBranch('wrong place')
    print('PASS')
except:
    print('FAIL')

print('manager.calculateIdleTimeOfTruck(): existing truck')
try:    
    manager.calculateIdleTimeOfTruck(1, '')
    print('PASS')
except:
    print('FAIL')

print('manager.calculateIdleTimeOfTruck(): non existing truck')
try:    
    manager.calculateIdleTimeOfTruck(2, '')
    print('PASS')
except:
    print('FAIL')

print('manager.viewTruckUsageInPeriod(): existing truck and correct date format')
try:    
    manager.viewTruckUsageInPeriod(1, '', '30/03/2020', '31/03/2020')
    print('PASS')
except:
    print('FAIL')

print('manager.viewTruckUsageInPeriod(): non existing truck')
try:    
    manager.viewTruckUsageInPeriod(2, '', '30/03/2020', '31/03/2020')
    print('PASS')
except:
    print('FAIL')

print('manager.viewTruckUsageInPeriod(): wrong date format')
try:    
    manager.viewTruckUsageInPeriod(2, '', '30/3/2020', '31/3/2020')
    print('PASS')
except:
    print('FAIL')

print('truck.changeDriver()')
try:
    truck.changeDriver('nameNew', 678, 'plate')
    truck.changeDriver('nameNew', 678, 'platewrong')
    print('PASS')
except:
    print('FAIL')

print('truck.dispatchTruck(): existing truck')
try:
    truck.dispatchTruck(1)
    print('PASS')
except:
    print('FAIL')

print('truck.dispatchTruck(): non existing truck')
try:
    truck.dispatchTruck(0)
    print('PASS')
except:
    print('FAIL')

print('consign.dispatchConsignment(): non existing consignment')
try:
    consign.dispatchConsignment(0, 1)
    print('PASS')
except:
    print('FAIL')

print('consign.dispatchConsignment(): existing consignment')
try:
    consign.dispatchConsignment(1, 1)
    print('PASS')
except:
    print('FAIL')

print('consign.loadConsignment(): non existing consignment')
try:
    consign.loadConsignment(0, truckObj)
    print('PASS')
except:
    print('FAIL')

print('consign.loadConsignment(): existing consignment but None dictionary')
try:
    consign.loadConsignment(1, None)
    print('PASS')
except:
    print('FAIL')

print('consign.loadConsignment(): existing consignment and wrong dictionary')
try:
    consign.loadConsignment(1, {'Plate Number': 'plate'})
    print('PASS')
except:
    print('FAIL')

print('consign.loadConsignment(): existing consignment and correct dictionary')
try:
    consign.loadConsignment(1, truckObj)
    print('PASS')
except:
    print('FAIL')

print('utility.loadUnloadedConsignments(): existing branch')
try:
    utility.loadUnloadedConsignments('Indore')
    print('PASS')
except:
    print('FAIL')

print('utility.loadUnloadedConsignments(): non existing branch')
try:
    utility.loadUnloadedConsignments('wrong place')
    print('PASS')
except:
    print('FAIL')