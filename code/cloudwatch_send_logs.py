"""
Send logs in AWS CloudWatch
"""

import boto3
import time

# Define variables
your_group = 'group_name'
your_stream = 'stream_name'

client = boto3.client("logs")

# Create log_group
response = client.create_log_group(
    logGroupName='your_group',
    kmsKeyId='string',
    tags={
        'string': 'string'
    }
)

# Create log_stream
response = client.create_log_stream(
    logGroupName='your_group',
    logStreamName='your_stream'
)

# Initialize function to get time
def get_time():
    timestamp = int(round(time.time() * 1000))
    return timestamp

# Initialize function to get a new token
def sequencetoken():
    logdescribe = btlog.describe_log_streams(logGroupName=your_group,logStreamNamePrefix=your_stream)
    logStreams = logdescribe['logStreams']
    logStream = logStreams[0]
    sequenceToken = logStream['uploadSequenceToken']
    return sequenceToken

# Send log
response = btlog.put_log_events(
    logGroupName='your_group',
    logStreamName='your_group',
    sequenceToken = sequencetoken(), # IMPORTANT -> if it's your first log you don't need sequencetoken()
    logEvents=[
        {
            'timestamp': get_time(),
            'message': time.strftime('%Y-%m-%d %H:%M:%S')+'\t : '+ data +' : Connexion AWS done'
        }
    ]
)
