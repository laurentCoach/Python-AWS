import json
import boto3
from datetime import datetime

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = 'table_name'  # Replace with your DynamoDB table name
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Get the current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    # Get the S3 event records
    records = event.get('Records', [])
    
    for record in records:
        # Retrieve the S3 bucket and key
        s3 = record['s3']
        bucket = s3['bucket']['name']
        key = s3['object']['key']
        s3_event = record.get('eventName', '')

        if s3_event.startswith('ObjectCreated:'):
            # Insert data into DynamoDB for ObjectCreated event
            version_id = s3['object'].get('versionId', '')  # Get the VersionId
            dynamodb_item = {
                'Filename': key,
                'VersionId': version_id,
                'Timestamp': current_time,
                'Bucket': bucket,
                'Key': key
            }
            # Insert the data into DynamoDB
            table.put_item(Item=dynamodb_item)
            # Print the data
            print(f"Inserted into DynamoDB: {dynamodb_item}")
        elif s3_event.startswith('ObjectRemoved:'):
            # This is a DELETE (object deletion) event
            version_id = record.get('s3', {}).get('object', {}).get('versionId', '')
            table.delete_item(
                TableName=table_name,
                Key={
                    'Filename': key,
                    'VersionId': version_id
                }
            )
            print(f"Object was deleted from DynamoDB for VersionId: {version_id}")

    return {
        'statusCode': 200,
        'body': json.dumps('S3 event processed successfully')
    }
