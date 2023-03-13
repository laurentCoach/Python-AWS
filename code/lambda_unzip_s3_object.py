import boto3
from io import BytesIO
import zipfile

# Function to unzip input Batch        
def unzip_input_batch(s3r, bucket_name_source, object):
    zip_obj = s3r.Object(bucket_name_source, key=object)

    buffer = BytesIO(zip_obj.get()["Body"].read())
    
    z = zipfile.ZipFile(buffer)
    for filename in z.namelist():
        file_info = z.getinfo(filename)
        s3r.meta.client.upload_fileobj(
            z.open(filename),
            Bucket=bucket_name_source,
            Key=f'input_data/{filename}'
        )
