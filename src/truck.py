import pymongo
import utility


class Truck:
    def __init__(self, numberPlate, CurrentLocation, DriverAsigned,Driver) -> None:
        self.numberPlate = numberPlate
        self.CurrentLocation = CurrentLocation
        self.DriverAsigned = DriverAsigned
        self.Driver = Driver
        

    def convertToDictAndUpload(self) -> None:
        utility.truckDB.insert_one({
            'numberPlate': self.numberPlate, 
            'CurrentLocation': self.CurrentLocation, 
            'DriverAsigned': self.DriverAsigned, 
            'Driver': self.Driver})
        