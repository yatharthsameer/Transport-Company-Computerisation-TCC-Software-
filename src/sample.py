import bill

consignSample = {
    '_id': id, 
    'Volume': 100,
    'Sender Name': 'sender', 
    'Sender Address': 'sender address',
    'Sender Phone': "sender phone", 
    'Receiver Name': 'reciever', 
    'Receiver Address': "reciever address", 
    'Receiver Phone': 'reciever phone',
    'Date Of Arrival': '20-03-12',
    'Date Of Dispatch': '23-03-12',
    'Cost': 10000
    }

bill.bill(consignSample)