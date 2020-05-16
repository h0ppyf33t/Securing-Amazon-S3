# Hello There,
# This project is a compilation of python scripts that hardens the security posture of an AWS S3 bucket.

# As we know all AWS S3 buckets are globally accessible via this endpoint http://<bucket_name>.s3.amazonaws.com.
# There are a few things you need enabled or tweaked to ensure whatever you put in your bucket is safe and secure.
#
# Here's what this project helps you automate:
# 1. Enable SSE (Server Side Encryption) for your bucket so data at rest are encrypted.
# 2. Adds a bucket policy to deny all non-https traffic to ensure data in transit is secure.
# 3. Enables bucket logging to ensure there is an audit trail to tract bucket access information.
#
# The send_to_sns module sends email notifications as and when the remediation takes place.
# v0.0.1

import json
import boto3
from sse import *
from bucket_policy import *
from bucket_logging import *

SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN','')

s3 = boto3.resource('s3')
def lambda_handler(event, context):
    text_output_array = ["-------------------------\n"]
    # I know this is not the perfect way to do this. LMK if you have another way to get the account number.
    ACCOUNT_ID = context.invoked_function_arn.split(":")[4]
    text_output_array.append("AWS ACCOUNT_ID: ")
    text_output_array.append(ACCOUNT_ID)
    text_output_array.append("\n")
    for bucket in s3.buckets.all():
        sse(bucket.name,SNS_TOPIC_ARN,text_output_array)
        bucket_policy(bucket.name,SNS_TOPIC_ARN,text_output_array)
        bucket_logging(SNS_TOPIC_ARN,text_output_array)
