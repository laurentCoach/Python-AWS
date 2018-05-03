"""
This code permits to update dynamoDB
"""

# Import library
import boto3
import pandas as pd

# Load connexion
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')

# Get item in the table
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
Table = dynamodb.Table('your_table')
response = Table.scan()
item=pd.DataFrame(response["Items"])

# Update dynamoDB
Update = Table.update_item(
                Key={'key_a': name_a,
                     'key_b':name_b
                     },
                     UpdateExpression="set last_refresh_date=:a,last_run_date=:b",
                     ExpressionAttributeValues={
                        ':a': a,
                        ':b': b
                    },
                    ReturnValues="UPDATED_NEW")
