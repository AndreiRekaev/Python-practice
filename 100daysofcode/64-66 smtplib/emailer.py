import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import omdb  # email json data from 40-42 days

from_addr = 'andreirekaev@gmail.com'
to_addr = 'andreirekaev@gmail.com'
bcc = ['']

msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = 'Movie info'

body = omdb.main()

msg.attach(MIMEText(body, 'plain'))

smtp_server = smtplib.SMTP('smtp.gmail.com', 587)

smtp_server.ehlo()

smtp_server.starttls()

smtp_server.login('andreirekaev@gmail.com', 'ID application')

text = msg.as_string()

smtp_server.sendmail(from_addr, [to_addr] + bcc, text)

smtp_server.quit()

print('Email sent succesfully')
