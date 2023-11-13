def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    s3_client = boto3.client('s3')

    # Specify the table name
    table_name = 'bucket_name'

    # Define the key to retrieve
    key = {
        'Filename': {'S': 'filename.ext'},
        'VersionId': {'S': 'verion_id'}
    }

    # Perform a GET request to retrieve an item
    response = dynamodb.get_item(TableName=table_name, Key=key)

    print('response:', response)
    
    # Extract and process the item from the response
    item = response.get('Item', [])
    print('item:', item)
    # Get the S3 bucket name and object key from the DynamoDB item
    bucket_name = item.get('Bucket', {}).get('S')
    print('bucket_name:', bucket_name)
    object_key = item.get('Key', {}).get('S')
    print('bucket_name:', object_key)
    
    # Use the bucket name and object key to read the content from S3
    try:
        s3_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        content = s3_response['Body'].read().decode('utf-8')
        print('File content:', content)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'FileContent': content})
        }
    except Exception as e:
        print('Error reading the file from S3:', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Error reading the file from S3')
        }
