import json
import boto3
from datetime import datetime
import csv
from io import StringIO
import os
import sys

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = 'table_name'  # Replace with your DynamoDB table name
table = dynamodb.Table(table_name)

def get_csv_columns(bucket, key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=key)
    
    # Read the first few lines of the CSV to get the header
    header_lines = response['Body'].read().decode('utf-8').split('\n')[:5]

    # Use CSV reader to parse the header
    csv_reader = csv.reader(StringIO('\n'.join(header_lines)))
    columns = next(csv_reader, [])
    
    return columns
    
def delete_old_versions(bucket, key, table, table_name, version_id, filename):
    s3_client = boto3.client('s3')
    
    # List all versions of the object
    versions = s3_client.list_object_versions(Bucket=bucket, Prefix=key)
    print('versions:', versions)

    for version in versions.get('Versions', []):
        if version['VersionId'] != version_id:
            # Delete the older versions in S3
            s3_client.delete_object(Bucket=bucket, Key=key, VersionId=version['VersionId'])
            
            # Delete the corresponding records in DynamoDB
            table.delete_item(
                TableName=table_name,
                Key={
                    'Filename': filename,
                    'VersionId': version['VersionId']
                }
            )
            print(f"Old version {version['VersionId']} deleted from S3 and DynamoDB")



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
        # Check if the key has a CSV file extension
        _, file_extension = os.path.splitext(key)
        filename = key.split('/')[-1]  

        version_id = s3['object'].get('versionId', '')  # Get the VersionId
        
        if s3_event.startswith('ObjectCreated:'):
            # Insert data into DynamoDB for ObjectCreated event
            
            if file_extension.lower() == '.csv':
                # Get CSV columns
                csv_columns = functions.get_csv_columns(bucket, key)
                
                dynamodb_item = {
                'Filename': filename,
                'VersionId': version_id,
                'Timestamp': current_time,
                'Bucket': bucket,
                'Key': key,
                'CsvColumns': csv_columns
                }
                # Insert the data into DynamoDB
                table.put_item(Item=dynamodb_item)
                # Print the data
                print(f"CSV file Inserted into DynamoDB: {dynamodb_item}")
            
            else:
                dynamodb_item = {
                    'Filename': filename,
                    'VersionId': version_id,
                    'Timestamp': current_time,
                    'Bucket': bucket,
                    'Key': key
                }
                # Insert the data into DynamoDB
                table.put_item(Item=dynamodb_item)
                # Print the data
                print(f"Other file Inserted into DynamoDB: {dynamodb_item}")
                
        # Check for 'DeleteMarkerCreated' event
        if s3_event.startswith('ObjectRemoved:DeleteMarkerCreated'):
            # Delete all older versions in S3 and DynamoDB
            print('DeleteMarkerCreated')
            functions.delete_old_versions(bucket, key, table, table_name, version_id, filename)
               
        elif s3_event.startswith('ObjectRemoved:Delete'):
            # This is a DELETE (object deletion) event
            version_id = record.get('s3', {}).get('object', {}).get('versionId', '')
            table.delete_item(
                TableName=table_name,
                Key={
                    'Filename': filename,
                    'VersionId': version_id
                }
            )
            print(f"Object was deleted from DynamoDB for VersionId: {version_id}")

    return {
        'statusCode': 200,
        'body': json.dumps('S3 event processed successfully')
    }
