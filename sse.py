import json
import boto3
import botocore
import os
from send_to_sns import *

s3_client = boto3.client('s3')

# Prepare your ServerSideEncryptionConfiguration json.
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_encryption
aes = {
    'Rules': [
        {
            'ApplyServerSideEncryptionByDefault': {
            'SSEAlgorithm': 'AES256'
            }
        },
	]
}

# Takes the bucketname, SNS_TOPIC_ARN for notification as input. Appends text_output_array with output.
def sse(bucket,SNS_TOPIC_ARN,text_output_array):
    # Check if the bucket already has encryption.
    try:
      encryption_status = s3_client.get_bucket_encryption(Bucket=bucket)
      print('Nothing to do for: %s' % bucket)
    # Add SSE and send event notification.
    except botocore.exceptions.ClientError as e:
          if e:
              s3_client.put_bucket_encryption(Bucket=bucket, ServerSideEncryptionConfiguration=aes)
              print('Added SSE for bucket: %s' % bucket)
              text_output_array.append("Added SSE for bucket:")
              text_output_array.append(bucket)
              text_output_array.append("\n")
              sendEvent(text_output_array,SNS_TOPIC_ARN)
