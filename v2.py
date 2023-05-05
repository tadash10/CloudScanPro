import os
import time
import logging
from typing import Dict

import requests


# Set up logging
logging.basicConfig(filename='api_calls.log', level=logging.INFO)

# Define constants
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

# Define API rate limits
GCP_RATE_LIMIT = 10  # 10 requests per second
AWS_RATE_LIMIT = 5  # 5 requests per second


def make_gcp_api_call(api_endpoint: str, api_key: str) -> Dict:
    """
    Makes an API call to the specified GCP endpoint using the provided API key.

    Returns:
        A dictionary representing the response from the API.
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.get(api_endpoint, headers=headers)

    # Handle errors
    if response.status_code != 200:
        logging.error(f'Error making GCP API call: {response.text}')
        raise Exception(f'Error making GCP API call: {response.status_code}')

    return response.json()


def make_aws_api_call(api_endpoint: str, aws_access_key: str, aws_secret_key: str) -> Dict:
    """
    Makes an API call to the specified AWS endpoint using the provided AWS access key and secret key.

    Returns:
        A dictionary representing the response from the API.
    """
    auth = (aws_access_key, aws_secret_key)
    response = requests.get(api_endpoint, auth=auth)

    # Handle errors
    if response.status_code != 200:
        logging.error(f'Error making AWS API call: {response.text}')
        raise Exception(f'Error making AWS API call: {response.status_code}')

    return response.json()


def make_gcp_api_calls(num_calls: int):
    """
    Makes a specified number of API calls to GCP endpoints.

    Raises:
        Exception: If the rate limit is exceeded.
    """
    # Calculate the delay between each API call
    delay = 1.0 / GCP_RATE_LIMIT

    for i in range(num_calls):
        # Make the API call
        api_endpoint = f'https://www.googleapis.com/compute/v1/projects/{GCP_PROJECT_ID}/zones/us-central1-a/instances'
        try:
            make_gcp_api_call(api_endpoint, 'fake_gcp_api_key')
            logging.info(f'Successfully made GCP API call {i+1}/{num_calls}')
        except Exception as e:
            logging.error(f'Error making GCP API call {i+1}/{num_calls}: {str(e)}')
            raise

        # Delay between API calls to avoid exceeding the rate limit
        if i < num_calls - 1:
            time.sleep(delay)


def make_aws_api_calls(num_calls: int):
    """
    Makes a specified number of API calls to AWS endpoints.

    Raises:
        Exception: If the rate limit is exceeded.
    """
    # Calculate the delay between each API call
    delay = 1.0 / AWS_RATE_LIMIT

    for i in range(num_calls):
        # Make the API call
        api_endpoint = 'https://ec2.amazonaws.com/?Action=DescribeInstances&Version=2016-11-15'
        try:
            make_aws_api_call(api_endpoint, AWS_ACCESS_KEY, AWS_SECRET_KEY)
            logging.info(f'Successfully made AWS API call {i+1}/{num_calls}')
        except Exception as e:
           
