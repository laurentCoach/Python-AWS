"""
Delete all files in s3
"""

# Import libary
import boto3

# Connexion AWS
s3c = boto3.client('s3')
s3 = boto3.resource('s3')

# Select bucket
my_bucket = s3.Bucket('my_bucket')

#delete file in bucket
my_bucket.objects.all().delete()
