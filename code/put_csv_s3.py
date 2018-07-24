Author : Laurent Cesaro

# Create a csv file in s3

# Load library
import boto 3

bucket = bucket_name
# AWS Connexion
s3 = boto3.resource('s3')
bucket_s3 = s3.Bucket(bucket_name)

# Create basic dataframe
df = pd.read_csv('...csv')

# Put csv file in s3
response = s3c.put_object(
         Bucket=bucket,
         Body=df.to_csv(None,index=False, header=False), # Here without index and header
         Key="subbucket/"+dfname+".csv"
         )
