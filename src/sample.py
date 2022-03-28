'''
import bill

consignSample = {
    '_id': id, 
    'Volume': 100,
    'Sender Name': 'Yash', 
    'Sender Address': '21, RK Nagar, Bangalore',
    'Sender Phone': "9853224324", 
    'Sender Mail': 'ytharthsmr@gmail.com',
    'Receiver Name': 'Jay', 
    'Receiver Address': "9, Bank Colony, Ratlam", 
    'Receiver Phone': '8623879463',
    'Date Of Arrival': '20-03-12',
    'Date Of Dispatch': '23-03-12',
    'Cost': 10000
    }

bill.bill(consignSample)
'''

from datetime import datetime
s1 = datetime.now()
s2 = datetime.strptime('2022-05-01 00:00:00', '%Y-%m-%d %H:%M:%S')
d = s2 - s1
d2 = s2 - s1
print(d + d2)
print(d.days * 24 + d.seconds / 3600)