import boto3

cloudwatch = boto3.client("cloudwatch", region_name="eu-west-1")


def send_custom_metric(name, val):
    cloudwatch.put_metric_data(
        MetricData=[
            {
                "MetricName": name,
                "Dimensions": [
                    {"Name": "Environment", "Value": "Development"},
                ],
                "Unit": "None",
                "Value": val,
            },
        ],
        Namespace="ATP/Metrics",
    )
