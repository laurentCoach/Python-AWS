"""
List sub_bucket in s3
List files in sub_bucket
Store them in AWS Lambda /tmp/ directory
"""

import boto3

# Connexion AWS
s3c = boto3.client('s3')
s3r = boto3.resource('s3')

## Bucket to use
bucket_name = "your_bucket"
bucket = s3r.Bucket(bucket_name)

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

# iterate in s3 subfolder
# Store file in AWS lambda tmp folder
for sub_ in sub:
    for obj in bucket.objects.filter(Delimiter='/', Prefix=sub_):
        obj = obj.key  # Get object ex: sub_bucket/your_file.csv

        path_l = obj.split('/')  # create list from obj

        path = path_l[1] + '/' + path_l[2]

        file = obj.split('/')[-1]  # Get file ex: your_file.csv
        
        # Create folder to store object in tmp
        if not os.path.isdir('/tmp/' + path):
            os.makedirs(path + '/')

        # load file from s3 to tmp directory
        s3r.meta.client.download_file(bucket_name, obj, '/tmp/' + path + '/' + file)
