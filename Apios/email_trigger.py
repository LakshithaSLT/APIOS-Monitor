import smtplib
import sqlalchemy as sql
import pandas as pd
import itertools
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Your Gmail login credentials
username = "testuweiot@gmail.com"
password = "nlqhmpcgvypioekv"

# The recipient's email address
to_email = "sltthenuwara@gmail.com"

# Create a new SMTP server instance
server = smtplib.SMTP("smtp.gmail.com", 587)

# Start the server's TLS (Transport Layer Security) mode
server.starttls()

# Log in to the server using your credentials
server.login(username, password)

last_sent = None

for i in itertools.count(start=1):
    # DB details
    db_url = "mysql+pymysql://uwe:uweproject@localhost/sensor_data"
    engine = sql.create_engine(db_url)
    connection = engine.connect()
    df = pd.read_sql_query('SELECT * FROM data_table', con=connection)
    result = df.loc[(df['Status'] == 'Critical')].tail(1)
    if (result.equals(last_sent) == False) and (df['Status'] == 'Critical').any():
        last_sent = result
        # Create the email message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Crtical Failure Alert - Apios Monitor"
        msg["From"] = username
        msg["To"] = to_email

        # Add the plain text body
        part1 = MIMEText(str(result), "plain")
        msg.attach(part1)

        # Add the HTML body
        html = """
        <html>
          <head></head>
          <body>
            <p>{0}</p>
          </body>
        </html>
        """.format(result.to_html())
        part2 = MIMEText(html, "html")
        msg.attach(part2)

        # Send the email
        server.sendmail(username, to_email, msg.as_string())
        print(f"Email Sent with  {result}")
    else:
        print ("Keep searching")
