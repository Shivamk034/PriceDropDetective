import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from typing import Union
from utils.logger import logging
import os
from dotenv import load_dotenv
load_dotenv()

sender_email = os.environ["SENDER_EMAIL"]

# Define the email sender function
def send_email(subject, body, recipients:Union[list,str]):
    if(isinstance(recipients,str)): recipients = [recipients]
    
    logging.info("Sending mail...")
    
    # Create a SendinBlue API configuration
    configuration = sib_api_v3_sdk.Configuration()

    # Replace "<your brevo api key here>" with your actual SendinBlue API key
    configuration.api_key['api-key'] = os.environ["BREVO_API_KEY"]

    # Initialize the SendinBlue API instance
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # SendinBlue mailing parameters
    subject = subject
    html_content = body
    sender = {"name": "Price Drop Detective", "email": sender_email}
    
    for recipient in recipients:
        
        to = [{"email":recipient}]
        # Create a SendSmtpEmail object
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

        try:
            # Send the email
            api_response = api_instance.send_transac_email(send_smtp_email)
            # print(api_response)
            logging.info("Email sent successfully!")
        except ApiException as e:
            logging.exception("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

        
if __name__=="__main__":
    receiver_email = os.environ["TEST_RECEIVER_EMAIL"]  # Enter receiver address
    # receiver_email = os.environ["ADMIN_EMAIL"]  # Enter receiver address
    message = """
    This message is sent from Python.
    """

    subject= "Price Just Dropped !!!"

    send_email(subject=subject,body=message,recipients=receiver_email)