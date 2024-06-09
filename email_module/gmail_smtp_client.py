import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()




sender_email = os.environ["SENDER_EMAIL"]
sender_password = os.environ["SENDER_EMAIL_PASSWORD"]

def send_email(subject:str, body:str, recipients:list|str):
    if(isinstance(recipients,str)): recipients = [recipients]
    
    
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender_email, sender_password)
       
       for recipient in recipients: # loop through the recipients List
            print("SENDING EMAIL")
            message = MIMEMultipart()  # Create user object
            message['Subject'] = subject
            message['From'] = sender_email
            message.attach(MIMEText(body, "plain"))
            message['To'] = recipient

            # print(message.as_string())
            
            smtp_server.sendmail(sender_email, recipient, message.as_string())
            
            print("Message sent!")



if __name__=="__main__":
    receiver_email = os.environ["TEST_RECEIVER_EMAIL"] 
 # of our text and
 # i think ye html mai bhi change ho jayega if we need to later
 # Enter receiver address
    # receiver_email = os.environ["ADMIN_EMAIL"]  # Enter receiver address
    message = """
    This message is sent from Python.
    """

    subject= "Price Just Dropped !!!"

    send_email(subject=subject,body=message,recipients=receiver_email)
