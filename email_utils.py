import smtplib, ssl
import os
from dotenv import load_dotenv
load_dotenv()

# port = 465  # For SSL
# smtp_server = "smtp.gmail.com"
# sender_email = os.environ["SENDER_EMAIL"]
# password = os.environ["SENDER_EMAIL_PASSWORD"]

# def send_email(receiver_email,message):
#     print("SENDING EMAIL")
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message)
 
#     print("SEND EMAIL")

# if __name__=="__main__":
#     receiver_email = ""  # Enter receiver address
#     message = """\
#     Subject: Hi there

#     This message is sent from Python."""

#     send_email(message=message,receiver_email=receiver_email)

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.
msg = EmailMessage()
msg.set_content("Hello!!!!!")

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = f'The contents of {'textfile'}'
msg['From'] = os.environ["SENDER_EMAIL"]
msg['To'] = ''

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()