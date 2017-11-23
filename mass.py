#TODO: Take emailid,password,filename as inputs
#TODO: Clean the data before writing to log.txt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from time import sleep
import re
import io

# Turn ON less secure apps for Gmail (https://www.google.com/settings/security/lesssecureapps)

try:
	s = smtplib.SMTP_SSL('smtp.domain.com', 465)
	# Gmail client identification
	# for TLS use port 587 and use smtplib.SMTP

	s.ehlo()
	# If using TLS, uncomment the line below.
	# s.starttls()

	s.login('username@mailprovider.com','password')
	s.set_debuglevel(1)
except IOError:
	print IOError

subject = """Dear Prof. """
body1 = """,
Lorem Ipsum Dolor""" 
body2 = """,
Lorem Ipsum Dolor""" 
sender = 'Name <username@mailprovider.com>'

names = []
field = []
recipients = []


# format Name,field,emailID
mailTxt = open("listOfRecipients.txt", 'r')

# Recipients being loaded
for line in mailTxt:
	line = line.replace('\n',"")
	names.append(re.split(',', line)[0])
	field.append(re.split(',',line)[1])
	recipients.append(re.split(',',line)[2])

for k in range(len(recipients)):
	msg = MIMEMultipart('mixed')
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = recipients[k]
	f = "file.extension"
	
	with open(f, "rb") as fil:
		part = MIMEApplication(
			fil.read(),
			Name=f
		)
	# For Attaching files
	part['Content-Disposition'] = 'attachment; filename="%s"',f
	msg.attach(part)
	#TODO: Write code for html as well
	part1 = MIMEText(salutation+names[k] + body1+field[k]+body2, 'text')
	msg.attach(part1)
	print "Sending..."
	
	
	try:
		s.sendmail(sender, recipients[k], msg.as_string())
	# Basic error handling: sometimes the SSL/TLS connection is interrupted which will stop the script. When this happens, it will try to reconnect, send the message, and continue the loop.
	except Exception, e:
		#TODO: Write a function for establishing connection
		print str(e) + "error: logging in and continuing loop with next address..."
		s = smtplib.SMTP_SSL('smtp.domain.com',465)
		s.ehlo()
		s.login('username@mailprovider.com','yourpassword')
		s.set_debuglevel(1)
		continue	
	
	with io.open('log.txt', 'a', encoding='utf-8') as f:
	  try:
	  	f.write(unicode(msg))
	  # As the code stands, it has trouble with accented characters. You might want to figure out a way to remove them or change the encoding of the script.
	  except:
		f.write("Error handling ASCII encoded names: "+ unicode(recipients[k]))
		
	print ("[*] "+ msg['To'])
	#Sleeping to avoid the mail being spent in spam
	print "Sleeping for 20 seconds..."
	sleep(20)

print "Mails Sent."
f.close()
s.quit()
