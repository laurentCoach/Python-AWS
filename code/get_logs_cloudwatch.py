# Autor : Laurent Cesaro
# Date : 23/01/2020

# Get logs from cloudwatch

#import library
import boto3

group = 'your_group'
stream = "your_stream"
AWS_REGION = "us-west-2"
query = None

client_log = boto3.client("logs", region_name=AWS_REGION)


# Get logs with query
def query_cloudwatch(group):
    query = "fields @timestamp, @message | filter @message | sort @timestamp desc"
    start_query_response = client_log.start_query(
        logGroupName=group,
        startTime=1577893839, # define time range
        endTime=1579621839, # see --> https://www.programiz.com/python-programming/time
        queryString=query,
    )

    query_id = start_query_response['queryId']
    response = None

    while response == None or response['status'] == 'Running':
        print('Waiting for query to complete ...')
        time.sleep(1)
        response = client_log.get_query_results(
            queryId=query_id
        )
    return response #return dict document


# Get number of log
def get_log_event(log_group, log_stream, nb, TorF): # Currently recover first logs not last
    resp = client_log.get_log_events(logGroupName=log_group, logStreamName=log_stream, limit=nb, startFromHead=TorF)
    resp = resp['events']
    get_msg = [d['message'] for d in resp]
    # return resp['events']
    return get_msg
