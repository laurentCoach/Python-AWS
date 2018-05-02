"""
Delete sub_bucket in a s3 bucket
"""

# Load library
import boto3

# AWS connexion
s3 = boto3.resource('s3')

# Define variables
bucket = "mybucket"
sub_bucket = "subbucket/"

# Delete sub_bucket and all his files
objects_to_delete = s3.meta.client.list_objects(Bucket=bucket, Prefix=sub_bucket)
delete_keys = {'Objects' : []}
delete_keys['Objects'] = [{'Key' : k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]
s3.meta.client.delete_objects(Bucket=bucket, Delete=delete_keys)
