import yfinance as yf
import datetime
import plotly.express as px
import pandas as pd
import os

# Define the stock ticker
ticker = "AAPL"
# Define the date range
end = datetime.date.today()
start = datetime.date.today() - datetime.timedelta(days=30)
# Get the stock data
stock = yf.download(ticker, start=start, end=end)

# DataFrame
df = pd.DataFrame(stock)
# set Index Name
df.index.name='Date'
df = df.reset_index()

# plotly
fig = px.line(df, x='Date', y='Close')
image_bytes = fig.to_image(format='png')

# Import modules
import smtplib, ssl
## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
### Add new subclass for adding attachments
from email.mime.application import MIMEApplication
## The pandas library is only for generating the current date, which is not necessary for sending emails
import pandas as pd

# Define the HTML document
# Add an image element
##############################################################
html = '''
    <html>
        <body>
            <h1>Last 30 days AAPL prices report</h1>
            <p>Hello, welcome to your report!</p>
            <img src='cid:myimageid' width="700">
        </body>
    </html>
    '''
##############################################################

# Define a function to attach files as MIMEApplication to the email
    ## Add another input extra_headers default to None
##############################################################
def attach_file_to_email(email_message, filename, extra_headers=None):
    # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
    # with open(filename, "rb") as f:
      file_attachment = MIMEApplication(image_bytes)
    # Add header/name to the attachments    
      file_attachment.add_header(
          "Content-Disposition",
          f"attachment; filename= {filename}",
      )
      # Set up the input extra_headers for img
        ## Default is None: since for regular file attachments, it's not needed
        ## When given a value: the following code will run
          ### Used to set the cid for image
      if extra_headers is not None:
          for name, value in extra_headers.items():
              file_attachment.add_header(name, value)
      # Attach the file to the message
      email_message.attach(file_attachment)
##############################################################    

# Set up the email addresses and password. Please replace below with your email address and password

email_from = 'bot.nebula9@gmail.com'
password = os.environ['PASSWORD']
email_to = 'naveenpraba08@gmail.com'
# Generate today's date to be included in the email Subject
date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

# Create a MIMEMultipart class, and set up the From, To, Subject fields
email_message = MIMEMultipart()
email_message['From'] = email_from
email_message['To'] = email_to
email_message['Subject'] = f'Report email-V2 - {date_str}'

# Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
email_message.attach(MIMEText(html, "html"))

# Attach more (documents)
  ## Apply function with extra_header on chart.png. This will render chart.png in the html content
##############################################################
attach_file_to_email(email_message, 'fig.png', {'Content-ID': '<myimageid>'})
##############################################################


# Convert it as a string
email_string = email_message.as_string()

# Connect to the Gmail SMTP server and Send Email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(email_from, password)
    server.sendmail(email_from, email_to, email_string) 
