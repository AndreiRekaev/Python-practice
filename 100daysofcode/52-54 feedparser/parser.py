import os.path
import smtplib
import feedparser
import xml.etree.ElementTree as ET
import mysql.connector
from configparser import ConfigParser


FEED_FILE = "newreleases.xml"
num_titles = 0

def parse_site():
  
  """Parse required data from web-site with feedparser"""
  
    new_releases = []
    feed = feedparser.parse(FEED_FILE)

    if 'title' in feed.entries[0]:
        for entry in feed.entries:
            new_releases.append(entry.published + " - " + entry.title + ": " + entry.link)
            global num_titles += 1
    return new_releases

def store_to_db():
  
  """INSERT data in database with sqlite3"""

    # give the connection parameters
    conn = mysql.connector.connect(user='root',
                                   password='',
                                   host='localhost',
                                   database='database')

    # reading
    tree = ET.parse('newreleases.xml')

    # item is the root for all data
    data2 = tree.findall('item')

    # retrieving the data and insert into table
    # i value for xml data #j value printing number of
    # values that are stored
    for i, j in zip(data2, range(num_titles)):
        name = i.find('title').text
        link = i.find('link').text
        date = i.find('pubDate').text

        # sql query to insert data into database
        data = """INSERT INTO newreleases(name, date, link) VALUES(%s,%s,%s)"""

        # creating the cursor object
        c = conn.cursor()

        # executing cursor object
        c.execute(data, (name, date, link))
        conn.commit()
        print("New release No-", j, " stored succesfully")

def send_email(to_addr, subject, text, encode='utf-8'):

    """Email sending"""

    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "email.ini")

    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Configuration not found!")

    server = cfg.get("smtp", "server")
    port = cfg.get("smtp", "port")
    from_addr = cfg.get("smtp", "email")
    passwd = cfg.get("smtp", "passwd")
    charset = f'Content-Type: text/plain; charset={encode}'
    mime = 'MIME-Version: 1.0'

    # body mail
    body = "\r\n".join((f"From: {from_addr}", f"To: {to_addr}",
            f"Subject: {subject}", mime, charset, "", text))

    try:
        # connecting to server
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.ehlo()
        # log-in
        smtp.login(from_addr, passwd)
        # sending e-mail
        smtp.sendmail(from_addr, to_addr, body.encode(encode))
    except smtplib.SMTPException as err:
        print("Something went wrong")
        raise err
    finally:
        smtp.quit()


if __name__ == '__main__':
    to_addr = ["person-one@gmail.com", "person-two@gmail.com", "person-three@gmail.com"]
    subject = "New releases from Steam"
    text = parse_site()
    send_email(to_addr, subject, text)
    store_to_db()
