from datetime import datetime
import pymongo
import utility


def branchQuery(branchName):
    return utility.branchDB.find_one({'Location': branchName})


def truckQuery(id, plate):
    if id != '':
        return utility.truckDB.find_one({'_id': int(id)})
    else:
        return utility.truckDB.find_one({'Number Plate': plate})

def employeeQuery(id, name):
    if id != '':
        return utility.employeeDB.find({'_id': int(id)})
    else:
        return utility.employeeDB.find({'Name': name})

def consignmentQuery(id, sendername, receiverName):
    if id != '':
        return utility.consignDB.find({'_id': int(id)})
    elif sendername != '':
        return utility.consignDB.find({'Sender Name': sendername, 'Receiver Name': sendername})
    else:
        return utility.consignDB.find({'Receiver Name': receiverName})

def queryConsignmentsHeadedToSameBranch(branchName):
    result = utility.consignDB.find({'Destination': branchName, 'Status': 'Dispatched'})
    revenue = 0
    for consign in result:
        revenue += consign['Cost']
    return revenue, result

def calculateIdleTimeOfTruck(id, plate):
    truck = truckQuery(id, plate)
    if len(truck['Delivery History']) == 0:
        return 24
    netIdleTime = utility.deltaTimeToHours(utility.stringToDateTime(truck['Date Of Purchase']), utility.stringToDateTime(truck['Delivery History'][0]['Dispatched At']))
    for i in range(len(truck['Delivery History'])-1):
        netIdleTime += utility.deltaTimeToHours(utility.stringToDateTime(truck['Delivery History'][i]['Delivered At']), utility.stringToDateTime(truck['Delivery History'][i+1]['Dispatched At']))
    if truck['Dispatched At'] == 'NA':
        netIdleTime += utility.deltaTimeToHours(utility.stringToDateTime(truck['Delivery History'][-1]['Delivered At']), utility.now())
    else:
        netIdleTime += utility.deltaTimeToHours(utility.stringToDateTime(truck['Delivery History'][-1]['Delivered At']), utility.stringToDateTime(truck['Dispatched At']))
    return netIdleTime

def viewTruckUsageInPeriod(id, plate, start, end):
    truck = truckQuery(id, plate)
    result = []
    start = datetime.strptime(start, '%d/%m/%Y')
    end = datetime.strptime(end, '%d/%m/%Y')
    for delivery in truck['Delivery History']:
        if utility.stringToDateTime(delivery['Dispatched At']) >= start and utility.stringToDateTime(delivery['Delivered At']) <= end:
            result.append(delivery)
    return result