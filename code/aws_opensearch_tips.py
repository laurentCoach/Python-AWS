import boto3
import time
import json

# From Layer
from opensearchpy import OpenSearch, RequestsHttpConnection  
from opensearchpy.helpers import bulk
import requests
import unicodedata


try:
  # Connexion
  client = OpenSearch(
      hosts = [{"host": "hostname", "port": 443}],
      http_auth = False,
      use_ssl = True,
      verify_certs = False,
      ssl_assert_hostname = False,
      ssl_show_warn = False,
      )
  print('{}: OpenSearch connection Success'.format(session))
except Exception as e:
  print('{}: ERROR: OpenSearch connection failed'.format(session))
  raise e
  
  
# Create index
response = client.indices.create('index-dev')
print('\nCreating index:')
print(response)
time.sleep(30)

# Insert data
body = {}  #Json Document
client.index(index="index-dev", body=body)

# Count total document in index
client.indices.refresh(index="index-dev")
print('Count total document in index')
print(client.cat.count(index="index-dev", format="json"))

# Search for the document.
response = client.search(
    index="index-dev",
        body={
            "size": 10000,
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "your_field": "Test",
                        }
                    },
                },
            },            
        } 
    )

print('Search results:')
print(response)
print('Total documents find')
print(response['hits']['total']['value'])


# delete documents
response = client.delete_by_query(
    index="index-dev",
    body ={
    "query": {
        "match": {
                "your_field": "Test",
                }
            }
        }
    )

# Delete index
client.indices.delete(index='index-dev')
print('Index properly deleted')

# Create Mapping
mapping = {
    'properties': {
        'your_field.param_1' : {'type': 'date', "format" : "yyyy-MM-dd HH:mm:ss.SSS"},
        'your_field.param_2' : {'type': 'date', "format" : "yyyy-MM-dd HH:mm:ss.SSS"}
        }
    }

# Create the mapping
response = client.indices.put_mapping(
    index='index-dev',
    body=mapping
)
