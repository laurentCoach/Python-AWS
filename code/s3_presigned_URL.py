import boto3

s3 = boto3.client('s3')

def generate_presigned_url(bucket_name, object_key, expiration=3600):
    try:
        response = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key
            },
            ExpiresIn=expiration
        )
        return response
    except Exception as e:
        print(f"An error occurred: {str(e)}")

bucket_name = 'your_bucket'
object_key = 'your_object.ext'
expiration_time = 300  # URL expiration time in seconds (1 hour)

presigned_url = generate_presigned_url(bucket_name, object_key, expiration_time)
print("Pre-signed URL:", presigned_url)
