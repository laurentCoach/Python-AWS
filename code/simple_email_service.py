# Autor: Laurent Cesaro
# Date: 19/02/2020

"""
Send emails with AWS Simple Email Service

In AWS SES define a SENDER

Email must have a HTML BODY
"""

# Libraries
import boto3
from botocore.exceptions import ClientError

# Variables
AWS_REGION = "your_region"


"""
Function to send email. 
Function Parameters:
  - email
  - html body
"""

def send_notification(recipients, BODY_HTML):
    global email_sent_status
    email_sent_status = False
    SENDER = "your.sender@y_s.com"
    RECIPIENT = recipients
    CHARSET = "UTF-8"

    # try to specific session id

    SUBJECT = "TEST SEND CRM EMAIL"

    client = boto3.client('ses', region_name=AWS_REGION)
    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
        email_sent_status = False
        return email_sent_status
    else:
        print("Email sent! Message ID:")
        print(response['MessageId'])
        email_sent_status = True
        return email_sent_status
