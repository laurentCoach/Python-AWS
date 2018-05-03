"""
List sub_bucket in s3
"""

import boto3

# Connexion AWS
s3c = boto3.client('s3')
s3 = boto3.resource('s3')

# Initialize Function
def list_folders(client, bucket, prefix=''):
    paginator = s3c.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter='/'):
        for prefix in result.get('CommonPrefixes', []):
            yield prefix.get('Prefix')

# Call Function
gen_subfolders = list_folders(s3c, 'my_bucket', prefix='sub_bucket/')
# Put all sub_folder in a list
sub = list(gen_subfolders)
