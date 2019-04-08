# Autor : Laurent Cesaro

import boto3
       
s3 = boto3.resource('s3')

## Bucket to use
bucket = s3.Bucket('bucket')

## List objects within a given prefix
for obj in bucket.objects.filter(Delimiter='/', Prefix='subfoler/'):
  print(obj.key)
