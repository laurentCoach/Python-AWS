"""
Read all CSV file in s3, except METADATA
"""

# Import library
import boto3
import pandas as pd
import io

# Connexion AWS
session = boto3.Session()
s3_client = session.client('s3')

# Select bucket
bucket = "my_bucket"
my_bucket = s3.Bucket('my_bucket')

list_file = []
list_stringcsv = []

# Iterate on all file in the bucket
for object in my_bucket.objects.all():
        stringcsv = object.key
        stringcsv = stringcsv.encode('ascii','ignore')
        
        if stringcsv not in list_stringcsv:
            if "metadata" not in stringcsv:
                list_file.append(stringcsv)
                obj = s3c.get_object(Bucket=bucket, Key=stringcsv)
                
                # Read File
                initial_df = pd.read_csv(io.BytesIO(obj['Body'].read()))
                list_stringcsv.append(stringcsv)

            else:
                continue
        else:
            continue
