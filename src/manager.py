import pymongo
import utility


def branchQuery(branchName):
    return utility.truckDB.find_one({'Location': branchName})


def truckQuery(query, isID = False):
    if isID:
        return utility.truckDB.find_one({'_id': query})
    else:
        return utility.truckDB.find_one({'Number Plate': query})

def employeeQuery(query, isID = False):
    if isID:
        return utility.employeeDB.find_one({'_id': query})
    else:
        return utility.employeeDB.find_one({'Name': query})

def consignmentQuery(id):
    return utility.consignmentDB.find_one({'_id': id})