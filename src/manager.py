from datetime import datetime
import pymongo
import utility


def branchQuery(branchName):        # returns branch object after searching
    return utility.branchDB.find_one({'Location': branchName})


def truckQuery(id, plate):          # returns truck object after searching via id or plate
    if id != '':
        return utility.truckDB.find_one({'_id': int(id)})
    else:
        return utility.truckDB.find_one({'Number Plate': plate})

def employeeQuery(id, name):            # returns employee list object after searching via id or name
    if id != '':
        return utility.employeeDB.find({'_id': int(id)})
    else:
        return utility.employeeDB.find({'Name': name})

def consignmentQuery(id, sendername, receiverName):         # returns consignment list object after searching via id or name of either sender or receiver
    if id != '':
        return utility.consignDB.find({'_id': int(id)})
    elif sendername != '':
        return utility.consignDB.find({'Sender Name': sendername, 'Receiver Name': sendername})
    else:
        return utility.consignDB.find({'Receiver Name': receiverName})

def queryConsignmentsHeadedToSameBranch(branchName):            # returns consignment list object after searching via branch name which are all headed to this branch
    result = list(utility.consignDB.find({'Destination': branchName, 'Status': 'Dispatched'}))
    revenue = 0
    for consign in result:
        revenue += consign['Cost']
    return revenue, result

def calculateIdleTimeOfTruck(id, plate):            # returns idle time of truck in hours / day
    truck = truckQuery(id, plate)
    if len(truck['Delivery History']) == 0:
        return 24
    netIdleTime = utility.deltaTimeToHours(utility.stringToDateTime(truck['Time Of Purchase']), utility.stringToDateTime(truck['Delivery History'][0]['Dispatched At']))
    for i in range(len(truck['Delivery History'])-1):
        netIdleTime += utility.deltaTimeToHours(utility.stringToDateTime(truck['Delivery History'][i]['Delivered At']), utility.stringToDateTime(truck['Delivery History'][i+1]['Dispatched At']))
    if truck['Dispatched At'] == 'NA':
        netIdleTime += utility.deltaTimeToHours(utility.stringToDateTime(truck['Delivery History'][-1]['Delivered At']), utility.stringToDateTime(utility.now()))
    else:
        netIdleTime += utility.deltaTimeToHours(utility.stringToDateTime(truck['Delivery History'][-1]['Delivered At']), utility.stringToDateTime(truck['Dispatched At']))
    return netIdleTime * 24 / utility.deltaTimeToHours(utility.stringToDateTime(truck['Time Of Purchase']), utility.stringToDateTime(utility.now()))

def viewTruckUsageInPeriod(id, plate, start, end):          # filters truck usage history and returns a list
    truck = truckQuery(id, plate)
    result = []
    start = datetime.strptime(start, '%d/%m/%Y')
    end = datetime.strptime(end, '%d/%m/%Y')
    for delivery in truck['Delivery History']:
        if utility.stringToDateTime(delivery['Dispatched At']) >= start and utility.stringToDateTime(delivery['Delivered At']) <= end:
            result.append(delivery)
    return result

def changeRate(newRate):
    utility.Rate = newRate