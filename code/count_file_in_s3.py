# Laurent Cesaro
# Date 05/10/2019

# Count file in specific s3 bucket

import boto3

s3 = boto3.client('s3')

response = s3.list_objects(
        Bucket='your-bucket',
        Prefix='path/to/your/folder/',
)
print(len(response['Contents']))
