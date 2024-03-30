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



def get_template_price_drop_email(name,product_name,product_url,previous_price,new_price,product_detail_url):

    prod_name_len = 20
    subject = f""" Price Drop Alert!  | {product_name[:prod_name_len]+("..." if len(product_name)>prod_name_len else "")}"""
    body = f"""
Hello, {name}

We are excited to inform you that the price of the product you have been monitoring has dropped!

Product Name: {product_name}
Previous Price: {previous_price}
New Price: {new_price}
Buy Product: {product_url}
Product Detail: https://shivam-kala-price-drop-detective.hf.space{product_detail_url}

Hurry up and grab this opportunity before the price changes again!

Thank you for using Price Drop Detective!

Best regards,
Your Price Drop Detective Team
 """

    return {
        "subject":subject,
        "body":body,
    }

# template =get_template_price_drop_email(name,product_name,product_url,previous_price,new_price,product_detail_url)
# send_email(subject=template["subject"],body=template["body"],recipients="asd")

if __name__=="__main__":
    receiver_email = os.environ["TEST_RECEIVER_EMAIL"]  # Enter receiver address
    # receiver_email = os.environ["ADMIN_EMAIL"]  # Enter receiver address
    message = """
    This message is sent from Python.
    """

    subject= "Price Just Dropped !!!"

    send_email(subject=subject,body=message,recipients=receiver_email)
