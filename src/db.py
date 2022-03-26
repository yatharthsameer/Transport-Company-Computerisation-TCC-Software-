import pymongo

cluster = pymongo.MongoClient("mongodb+srv://selabproject:selabproject@se.hl6lf.mongodb.net/TCC?retryWrites=true&w=majority")

db = cluster['TCC']
#col = db["Branch"]
#col.insert_one({'_id': 1, 'Location':'New Delhi', 'Address':'PK nagar, New Delhi', 'Number Of Employees': 1, 'Employees': [1], 'Revenue': 0})

col = db['Settings']
col.insert_one({'_id':0, 'BranchID':1, 'employeeID':1, 'truckID':1, 'consignID':1, 'managerID':'admin', 'managerPassword':'admin'})