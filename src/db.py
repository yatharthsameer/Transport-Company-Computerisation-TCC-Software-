import pymongo

cluster = pymongo.MongoClient("mongodb://selabproject:selabproject@se-shard-00-00.hl6lf.mongodb.net:27017,se-shard-00-01.hl6lf.mongodb.net:27017,se-shard-00-02.hl6lf.mongodb.net:27017/TCC?ssl=true&replicaSet=atlas-ee0z3v-shard-0&authSource=admin&retryWrites=true&w=majority")

database = cluster['TCC']

###### USE FOR RESETTING THE DATABASE ######
database['Settings'].delete_many({})
database['Employee'].delete_many({})
database['Branch'].delete_many({})
database['Consignment'].delete_many({})
database['Truck'].delete_many({})
database['Settings'].delete_many({})
database['Settings'].insert_one({'_id':0, 'BranchID':1, 'employeeID':1, 'truckID':1, 'consignID':1, 'managerID':'admin', 'managerPassword':'admin'})