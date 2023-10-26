import boto3
import json
from botocore.exceptions import ClientError

def get_secret(env):
    """Retrieves the Alpaca API Key from the AWS Secrets Manager Service

    Args:
        env (str): Environment (PAPER or REAL)

    Returns:
        dict: Alpaca API Key/Value Pair
    """

    if env == "REAL":
        secret_name = "prod/Alpaca_Key"
    elif env == "PAPER":
        secret_name = "paper/Alpaca_Key"
    region_name = "eu-west-1"

    session = boto3.session.Session()
    client = session.client(
        service_name = 'secretsmanager',
        region_name = region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
    else:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)