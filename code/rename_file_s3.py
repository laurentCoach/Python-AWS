"""
  Rename a file in a s3 repository
"""

# Load library
import boto3

# Connexion AWS - ressource
s3 = boto3.resource('s3')

# Copy the old file
s3.Object('my_bucket','my_file_new').copy_from(CopySource='my_bucket/my_file_old')

# Delete old file
s3.Object('my_bucket','my_file_old').delete()
