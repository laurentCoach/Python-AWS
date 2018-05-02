"""
Launch a request in Athena
"""

# Import library
import boto3

# Differents connexions
# s3
s3c = boto3.client('s3')
s3 = boto3.resource('s3')
# Athena
client = boto3.client('athena')

# s3 output for metadata
s3_output = 's3://bucket/metadata/'

# Initialize a query
query """select * from database.table limit 10;"""

# Launch query
response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': "database"
            },
        ResultConfiguration={
            'OutputLocation': s3_output,
            }
        )
        
# If the query take a lot of time
# Get the status of the request
query_execution_id = response['QueryExecutionId']
query_status = client.get_query_execution(QueryExecutionId=query_execution_id)
query_execution_status = query_status['QueryExecution']['Status']['State']

# If the status is RUNNING
# Continue until SUCEDEED or FAILED
while query_execution_status == 'RUNNING':
    query_execution_id = response['QueryExecutionId']
    query_status = client.get_query_execution(QueryExecutionId=query_execution_id)
    query_execution_status = query_status['QueryExecution']['Status']['State']
    
if query_execution_status == 'SUCCEEDED':
        print("Query Suceeded")
    else:
        print("Query Failed")
