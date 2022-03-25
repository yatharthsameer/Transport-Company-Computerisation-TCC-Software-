import pymongo

cluster = pymongo.MongoClient("mongodb://selabproject:selabproject@se-shard-00-00.hl6lf.mongodb.net:27017,se-shard-00-01.hl6lf.mongodb.net:27017,se-shard-00-02.hl6lf.mongodb.net:27017/TCC?ssl=true&replicaSet=atlas-ee0z3v-shard-0&authSource=admin&retryWrites=true&w=majority")

db = cluster['TCC']
#col = db["Branch"]
#col.insert_one({'_id': 1, 'Location':'New Delhi', 'Address':'PK nagar, New Delhi', 'Number Of Employees': 1, 'Employees': [1], 'Revenue': 0})

col = db['Settings']
col.insert_one({'_id':0, 'BranchID':1, 'employeeID':1, 'truckID':1, 'consignID':1, 'managerID':'admin', 'managerPassword':'admin'})