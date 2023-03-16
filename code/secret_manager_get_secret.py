import boto3
from botocore.exceptions import ClientError
import json, os
import sys
import base64
import time


def getCredentials():
    credential = {}
    secret_name = "secret_name"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session_boto3 = boto3.session.Session()

    smc = session_boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = smc.get_secret_value(
            SecretId=secret_name
        )

        secret = json.loads(get_secret_value_response['SecretString'])

        credential['username'] = secret['username']
        credential['password'] = secret['password']

    except Exception as e:
        print('ERROR in function getCredentials')
        print('{}: ERROR: in function getCredentials: {}'.format(session, e))
        raise e

    return credential
  
credentials = secret_manager.getCredentials()
