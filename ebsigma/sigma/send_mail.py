import smtplib
from email.mime.text import MIMEText

import sys
from time import sleep

def send_mail(receiver, id):
  username = 'YOUR EMAIL USER KEY'
  password = 'YOUR EMAIL USER PASSWORD'
  smtp_server = 'email-smtp.us-west-2.amazonaws.com'
  smtp_port = 587

  fromaddr = 'YOUR USER NAME@YOUR EMAIL DOMAIN'
  toaddrs = receiver
  msg = '''Subject: Your SigmaW results are in!\n\nYour SigmaW results can be found here: YOUR SITE DOMAIN/results/''' + id
  server = smtplib.SMTP(smtp_server, smtp_port, 10)

  server.starttls()
  server.ehlo()
  server.login(username, password)
  server.sendmail(fromaddr, toaddrs, msg)
  return server.quit()  
  
if __name__ == '__main__':
  send_mail(sys.argv[1], sys.argv[2])