import urllib.request
import json
import os
import ssl
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

stop_words = set(stopwords.words('english'))

def preprocess_data(message):
    # Preprocess the data
    message = re.sub(r'[^\w\s]', '', message)
    message = re.sub(r'[0-9]', '', message)
    message = message.lower()
    message = message.strip()
    message = word_tokenize(message)
    message = [word for word in message if not word in stop_words]
    ps = PorterStemmer()
    message = [ps.stem(word) for word in message]
    message = ' '.join(message)

    return message

def allowSelfSignedHttps(allowed):
    # Bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def call_endpoint(message):
    allowSelfSignedHttps(True)  # This line is needed if you use self-signed certificate in your scoring service.

    # Request data goes here
    data = {
        "input_data": {"Message": message},
        "params": {}
    }

    body = str.encode(json.dumps(data))

    url = 'https://email-spam-endpoint-fc10bd90.eastasia.inference.ml.azure.com/score'
    # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
    api_key = 'vbimdSOoZpQK0iJlGHuu2qStGY271MQE'

    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key,
        'azureml-model-deployment': 'berdebar'
    }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        return None

