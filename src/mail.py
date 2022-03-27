'''
import smtplib

email = "atulyaankitsharma@kgpian.iitkgp.ac.in"
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("grp10diy@gmail.com", "diyproject")
server.sendmail("testpython@test.com", email, "Hello")
server.quit()
'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


sender_address = 'grp10diy@gmail.com'
sender_pass = 'diyproject'


def sendMail(receiverAddress, billing = False, password = None):
    if billing:
        mail_content = '''Hello,
        This is an auto mail sent by TCC Services.
        Kindly see the billing of your consignment in the attachment.
        Thank You
        '''
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiverAddress
        message['Subject'] = 'TCC Billing'

        message.attach(MIMEText(mail_content, 'plain'))
        attach_file_name = 'bill.pdf'
        attach_file = open(attach_file_name, 'rb')
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) 

        payload.add_header('Content-Disposition', 'attachment; filename = %s' % attach_file_name)
        message.attach(payload)

        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiverAddress, text)
        session.quit()
    else:
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        session.sendmail("testpython@test.com", receiverAddress, "This is your new password for TCC Log In. DO NOT SHARE WITH ANYONE.\n" + password)
        session.quit()