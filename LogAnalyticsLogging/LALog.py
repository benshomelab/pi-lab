import json
import requests
import datetime
import hashlib
import hmac
import base64
import sys

# This script is an altered version of the example python request available at the following link:
# https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-collector-api#python-sample
# The main change is addition of the 'send_log' function.

sys.path.append('/usr/local/lib/python3.9/dist-packages/')

# Update the customer ID to your Log Analytics workspace ID
customer_id = '<workspace ID>'

# For the shared key, use either the primary or the secondary Connected Sources client authentication key   
shared_key = "<workspace key>"

# Build the API signature
def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
        x_headers = 'x-ms-date:' + date
        string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
        bytes_to_hash = bytes(string_to_hash, encoding="utf-8")  
        decoded_key = base64.b64decode(shared_key)
        encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
        authorization = "SharedKey {}:{}".format(customer_id,encoded_hash)
        return authorization
        
# Build and send a request to the POST API
def post_data(customer_id, shared_key, body, log_type, action):
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)
    uri = 'https://' + customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }
    #print('Posting with URI: ' + uri)
    #print('Body: ' + body)
    #print('Headers: ' + str(headers))
    response = requests.post(uri,data=body, headers=headers)
    if (response.status_code >= 200 and response.status_code <= 299):
        print('Sending log to LAW: ' + action)
    else:
        print("Log POST Response code: {}".format(response.status_code))

# This function us what is intended to be used to post data. See exammple below
def send_log(table, column, data):
    # This JSON determines the schema of the table. This can be changes as desired to meet you needs.
    json_data = [{
       "TimeGenerated": datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
       column: data
    }]
    body = json.dumps(json_data)
    post_data(customer_id, shared_key, body, table, data)
 
# Example of how to use the send_log function
#send_log('tableName','columnName','columnData')
