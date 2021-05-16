import requests
import json

#headers={ 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36' }
#This is your response header, replace the above value with the header, from the network tab in your web-console

pincode='560035'  
#this is the pincode which you will be receiving updates on

requestdate= datetime.today().strftime('%d-%m-%Y')

url='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode='+pincode+'&date=' +requestdate

res = requests.get(url,headers=headers)

#res = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=400607&date=16-05-2021',headers=headers)


#this returns a list of n hospitals
hospitals=res.json()["centers"]  

#we iterate through every hospital, each list item is a dictionary

#Sample responses
#3 items correspond to 3 different hospitals, each having >=1 slots
#{u'from': u'10:00:00', u'state_name': u'Karnataka', u'to': u'13:00:00', u'sessions': [{u'min_age_limit': 45, u'available_capacity_dose1': 0, u'available_capacity': 0, u'session_id': u'db08ac70-f728-44a9-9e79-00e048c25003', u'date': u'16-05-2021', u'slots': [u'10:00AM-12:00PM', u'12:00PM-01:00PM'], u'available_capacity_dose2': 0, u'vaccine': u'COVISHIELD'}, {u'min_age_limit': 45, u'available_capacity_dose1': 0, u'available_capacity': 0, u'session_id': u'a0bb61f8-db3b-414b-b027-b8de4d796b2b', u'date': u'17-05-2021', u'slots': [u'10:00AM-11:00AM', u'11:00AM-12:00PM', u'12:00PM-01:00PM', u'01:00PM-04:00PM'], u'available_capacity_dose2': 0, u'vaccine': u'COVISHIELD'}], u'center_id': 249066, u'pincode': 560035, u'long': 77, u'fee_type': u'Free', u'block_name': u'Bengaluru East', u'address': u'Sarjapura Main Road', u'lat': 12, u'district_name': u'Bangalore Urban', u'name': u'Halanayakanahalli PHC'}
#{u'from': u'10:00:00', u'state_name': u'Karnataka', u'to': u'16:00:00', u'sessions': [{u'min_age_limit': 45, u'available_capacity_dose1': 0, u'available_capacity': 0, u'session_id': u'e7c37206-cdda-4474-b8ad-a4a383bf8694', u'date': u'16-05-2021', u'slots': [u'10:00AM-11:00AM', u'11:00AM-12:00PM', u'12:00PM-01:00PM', u'01:00PM-04:00PM'], u'available_capacity_dose2': 0, u'vaccine': u'COVISHIELD'}], u'center_id': 406875, u'pincode': 560035, u'long': 77, u'fee_type': u'Free', u'block_name': u'West', u'address': u'Janatha Colony, Chikkabellandur, Bengaluru', u'lat': 12, u'district_name': u'BBMP', u'name': u'Doddakannalli UPHC P3'}
#{u'from': u'10:00:00', u'state_name': u'Karnataka', u'to': u'16:00:00', u'sessions': [{u'min_age_limit': 45, u'available_capacity_dose1': 0, u'available_capacity': 0, u'session_id': u'e3c84047-da95-4187-b588-dadd25d8bd4e', u'date': u'17-05-2021', u'slots': [u'10:00AM-11:00AM', u'11:00AM-12:00PM', u'12:00PM-01:00PM', u'01:00PM-04:00PM'], u'available_capacity_dose2': 0, u'vaccine': u'COVISHIELD'}], u'center_id': 249076, u'pincode': 560035, u'long': 77, u'fee_type': u'Free', u'block_name': u'Bengaluru East', u'address': u'Ambedkarnagar', u'lat': 12, u'district_name': u'Bangalore Urban', u'name': u'KODATHI PHC'}


class Hospital:
  def __init__(self, name, dose1, dose2, slot, vaccine):
    self.name = name.encode("utf-8")
    self.dose1 = str(dose1).encode("utf-8")
    self.dose2 = str(dose2).encode("utf-8")
    self.slot  = slot.encode("utf-8")
    self.vaccine = vaccine.encode("utf-8")

list=[]

for item in hospitals:
    #this is a dictionary
    itemvalues=item.values()
    fromItem=itemvalues[0]
    state_name=itemvalues[1]
    to=itemvalues[2]
    sessions=itemvalues[3]
    center_id=itemvalues[4]
    pincode=itemvalues[5]
    long=itemvalues[6]
    fee_type=itemvalues[7]
    block_name=itemvalues[8]
    address=itemvalues[9]
    lat=itemvalues[10]
    district_name=itemvalues[11]
    name=itemvalues[12]
    for thing in sessions:
        dose1 = thing['available_capacity_dose1']
        sDate = thing['date']
        slots = thing['slots']
        dose2 = thing['available_capacity_dose2']
        vaccine = thing['vaccine']
        for slot in slots:  
            #print name + " " + "slot time = " + slot  + " available dose1 = " + str(dose1) + " available dose 2 = " + str(dose2) + " " +vaccine
            list.append(Hospital(name,dose1,dose2,slot,vaccine))


availabilitylist=''
for obj in list:
    #print(obj.name, obj.dose1, obj.dose2, obj.slot, obj.vaccine)
    #add condition here, for Avalibility, if dose1 or dose2 >0 append to availabilitylist
    #this is not done now to simply test mail functionality
    availabilitylist = availabilitylist + obj.name + " dose1 remaining: " + obj.dose1 +  " dose2 remaining: " + obj.dose2 +  " " + obj.slot +  " " + obj.vaccine +"\n"

#enable messages from less secure accounts in gmail - https://support.google.com/accounts/answer/6010255

#Start a local smtp server in your shell
#python -m smtpd -c DebuggingServer -n localhost:1025

import smtplib, ssl

#Create a connection to GMAIL Mail server, the protocol for mail submission actually uses 587
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    #upgrading to a tls connection for security
except:
    print 'Something went wrong...'

sent_from='you@gmail.com'
to =['destemail@gmail.com'] 
#enter sender and destination email above 

subject='Vaccination Avalibility Alert!!!'
body=availabilitylist

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

gmail_user = 'enteryour@gmail.com'
gmail_password = 'enteryourpassword'

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
    print 'Email sent!'
except:
    print 'Something went wrong...'


