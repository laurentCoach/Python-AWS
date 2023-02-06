s3c = boto3.client('s3')
    
put_tags_response = s3c.put_object_tagging(
Bucket='BUCKET_NAME',
Key='PREFIX/OBJECT.EXT',    
Tagging={
    'TagSet': [
        {
            'Key': 'Key-Value',
            'Value': 'ValueValue'
        }
    ]
}
)
