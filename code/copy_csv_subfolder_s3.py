# Author : Laurent Cesaro
# Copy csv from s3 subfolder in an other s3 or same

# Load library
import boto3

# Define viriables
old_bucket_name = 'SRC'
old_prefix = 'A/B/C/'
new_bucket_name = 'TGT'
new_prefix = 'L/M/N/'

# AWS Connexion
s3 = boto3.resource('s3')
old_bucket = s3.Bucket(old_bucket_name )
new_bucket = s3.Bucket(new_bucket_name )

# Copy file
for obj in old_bucket.objects.filter(Prefix=old_prefix):
    old_source = { 'Bucket': old_bucket_name,
                   'Key': obj.key}
    # replace the prefix
    new_key = obj.key.replace(old_prefix, new_prefix)
    new_obj = new_bucket.Object(new_key)
    new_obj.copy(old_source)
