import boto3
import pandas

os.chdir("/tmp/")
bucket_name = 'your_bucket_name'

s3r = boto3.resource('s3')  
s3c = boto3.client('s3')

bucket = s3r.Bucket(bucket_name)
sub_ = 'sub_directory/'

for obj in bucket.objects.filter(Delimiter='/', Prefix=sub_):  #iterate over all file in bucket/sub_directory
    obj = obj.key  # class str

    file = obj.split('/')[-1]
    
    if file != '':
        s3r.meta.client.download_file(bucket_name, obj, '/tmp/'+file)  #download file to tmp directory
        df = pd.read_csv('/tmp/'+file)  # read csv

        df.rename(columns={'col_1': 'col_1_rename', 'col_2': 'col_2_rename'}, inplace=True)
        df.to_csv('/tmp/'+file, sep=',', index= False)  #save to csv

        s3c.upload_file('/tmp/'+file, bucket_name, sub_ + file)  #reload in s3 and overwrite previous csv file
