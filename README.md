# Transport Company Computerisation (TCC) Software
SE Lab Project

For running the code:

1. Install Libraries:\
    1.1 PyQt5\
    1.2 pymongo\
    1.3 matplotlib\
    1.4 dnspython\
    1.5 geopy\
    1.6 Nominatim\
    1.7 reportlab\
    1.8 pymongo[srv]\

2. (Optional) First run db.py to reset the database if required

3. Run main.py

4. Always put reciever's address in a format: 'anywhere, somewhere, City'. The city must be especially writted after a ', ' only.

5. Make sure that all cities mentioned in Branch, reciever address must be a real city.

6. Always initialise trucks in a branch city only.

7. For the sake of simplicity, use 'admin' as both username and password to enter as manager.

8. Put actual emails for employees or you will not have any idea about the password, since no one sees them.

9. After any truck is dispatched, you will recieve a system alert that the truck has dispatched. These will be go to respective destinations, and you need to accept these trucks as an employee of the destination branch, which will prompt the truck to unload at the destination.