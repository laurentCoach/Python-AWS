"""
Autor: Laurent Cesaro
Date: 29/01/2020

Class cloudwatch to send & get log in AWS cloudwatch

In your main file -
- import --> from cloudwatch import _CloudWatch
- create an object --> cloudwatch = _CloudWatch(session, AWS_REGION, group, stream)
- call function --> cloudwatch.send_cloudwatch_log_message("HELLO WORLD")
"""

# Import libraries
import time
import boto3
from botocore.exceptions import ClientError


class _CloudWatch:
    def __init__(self, session, AWS_REGION, group, stream):
        self.session = session
        self.client = boto3.client("logs", region_name=AWS_REGION)
        self.group = group
        self.stream = stream

    # Initialize function to get time
    def get_time(self):
        self.timestamp = int(round(time.time() * 1000))
        return self.timestamp

    def sequencetoken(self):
        logdescribe = self.client.describe_log_streams(logGroupName=self.group, logStreamNamePrefix=self.stream)
        logStreams = logdescribe['logStreams']
        logStream = logStreams[0]
        sequenceToken = logStream['uploadSequenceToken']
        return sequenceToken

    def send_cloudwatch_log_message(self, message=None):
        try:
            response = self.client.put_log_events(
                logGroupName=self.group,
                logStreamName=self.stream,
                sequenceToken=sequencetoken(self), # IMPORTANT -> if it's your first log you don't need sequencetoken()
                logEvents=[
                    {
                        'timestamp': self.get_time(),
                        'message': 'SID= {} INFO= {} ST={}'.format(self.session, message, self.sequencetoken())
                    }
                ]
            )
        except ClientError as ex:
            print("########################")
            error = ex.response['Error']['Message']
            next_token = error.split()
            next_token = next_token[-1] # Get the next token
            print(next_token)
            print("########################")
            response = self.client.put_log_events(
                logGroupName=self.group,
                logStreamName=self.stream,
                sequenceToken=next_token,
                logEvents=[
                    {
                        'timestamp': self.get_time(),
                        'message': 'SID= {} INFO= {} ST={}'.format(self.session, message, self.sequencetoken())
                    }
                ]
            )

    # Function to send WARNING & ERROR logs
    def send_cloudwatch_log_error(self, error=None):
        try:
            response = self.client.put_log_events(
                logGroupName=self.group,
                logStreamName=self.stream,
                sequenceToken=sequencetoken(self), # IMPORTANT -> if it's your first log you don't need sequencetoken()
                logEvents=[
                    {
                        'timestamp': self.get_time(),
                        'message': 'SID= {} ERROR= {} ST={}'.format(self.session, message, self.sequencetoken())
                    }
                ]
            )
        except ClientError as ex:
            print("########################")
            error = ex.response['Error']['Message']
            next_token = error.split()
            next_token = next_token[-1] # Get the next token
            print(next_token)
            print("########################")
            response = self.client.put_log_events(
                logGroupName=self.group,
                logStreamName=self.stream,
                sequenceToken=next_token,
                logEvents=[
                    {
                        'timestamp': self.get_time(),
                        'message': 'SID= {} INFO= {} ST={}'.format(self.session, error, self.sequencetoken())
                    }
                ]
            )

    # Function to query logs in cloudwatch. Need a delay between insertion and query
    def get_log_event(self):
        query = "fields @timestamp, @message | filter @message like /{}/ | sort @timestamp asc".format(self.session)
        print(query)
        start_query_response = self.client.start_query(
            logGroupName=self.group,
            startTime=int(time.time() - 100000),  # define time range
            endTime=int(time.time()),
            queryString=query,
        )

        query_id = start_query_response['queryId']
        response = None

        while response == None or response['status'] == 'Running':
            time.sleep(1)
            response = self.client.get_query_results(
                queryId=query_id
            )
        return response  # return dict document
