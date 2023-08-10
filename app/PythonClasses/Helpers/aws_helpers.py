import base64
import boto3
from botocore.exceptions import NoCredentialsError

def get_secret(secret_name, region_name="us-west-2"):
# The `get_secret` function is a Python function that retrieves a secret value from AWS Secrets
# Manager. It takes in two parameters: `secret_name` (the name or ARN of the secret) and
# `region_name` (the AWS region where the secret is stored, defaulting to "us-west-2").

    # Initialize a session using Amazon S3
    session = boto3.session.Session()
    
    # Create a Secrets Manager client
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    try:
        # Use the client to retrieve the secret value
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except NoCredentialsError:
        print('Credentials are not available.')
        return None

    # Depending on whether the secret is a string or binary, one of these fields will be populated
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        # Decode the binary secret string and return it
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        
    return secret