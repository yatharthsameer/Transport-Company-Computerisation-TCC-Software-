import pymongo
import utility


def branchQuery(branchName):
    return utility.truckDB.find_one({'Location': branchName})


def truckQuery(id, plate):
    if id != '':
        return utility.truckDB.find_one({'_id': int(id)})
    else:
        return utility.truckDB.find_one({'Number Plate': plate})

def employeeQuery(id, name):
    if id != '':
        return utility.employeeDB.find_one({'_id': int(id)})
    else:
        return utility.employeeDB.find_one({'Name': name})

def consignmentQuery(id, sendername, receiverName):
    if id != '':
        return utility.consignmentDB.find_one({'_id': int(id)})
    elif sendername != '':
        return utility.consignmentDB.find_one({'Sender Name': sendername, 'Receiver Name': sendername})
    else:
        return utility.consignmentDB.find_one({'Receiver Name': receiverName})