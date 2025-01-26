import boto3

# AWS Bedrock Configuration
bedrock_client = boto3.client("bedrock-runtime", "ap-south-1")

# Classification Threshold
CONFIDENCE_THRESHOLD = 0.75