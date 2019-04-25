import boto3
import botocore
import json
import os
from send_to_sns import *

s3_client = boto3.client('s3')

def bucket_policy(bucket,SNS_TOPIC_ARN,text_output_array):
    secure_bucket_policy = []
    policy = []
    append_bucket_policy = []
    # If the bucket policy is empty.
    secure_bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Deny",
                   "Principal": "*",
                    "Action": "s3:*",
                    "Condition": {
                        "Bool": {
                            "aws:SecureTransport": "false"
                        }
                    },
                    "Resource": "arn:aws:s3:::%s/*" % bucket
                }
            ]
        }
    # Just the deny stanza for an existing policy.
    append_bucket_policy = {
           "Effect": "Deny",
           "Principal": "*",
           "Action": "s3:*",
           "Condition": {
           "Bool": {
             "aws:SecureTransport": "false"
             }
        },
           "Resource": "arn:aws:s3:::%s/*" % bucket
     }
    # Convert them to string. https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_policy
    str_secure_bucket_policy=json.dumps(secure_bucket_policy)
    str_append_bucket_policy = json.dumps(append_bucket_policy)
    try:
         ori_bucket_policy = s3_client.get_bucket_policy(Bucket=bucket)
         policy = json.loads(ori_bucket_policy['Policy'])
         str_policy = json.dumps(policy)
         str_append_bucket_policy = str_append_bucket_policy.strip('[]')
         check = '{"Bool": {"aws:SecureTransport": "false"}}'
         # Check if the bucket already has the deny rule.
         if check in str_policy:
            print('Nothing to do for bucket: %s' % bucket)
         # Magic :P.
         # Since there is no boto3 api to append a stanza to an existing policy, the following is a work-a-round to shove append_bucket_policy in ori_bucket_policy.
         else:
             i = str_policy.find('[')
             try:
                 str_policy = str_policy[:i+1] + str_append_bucket_policy + ',' + str_policy[i+1:]
                 s3_client.put_bucket_policy(Bucket=bucket,Policy=str_policy)
                 print('Added secure policy to existing bucket policy for bucket: %s' % bucket)
                 text_output_array.append("Modified existing policy with secure policy for bucket: ")
                 text_output_array.append(bucket)
                 text_output_array.append("\n")
                 sendEvent(text_output_array,SNS_TOPIC_ARN)
             except botocore.exceptions.ClientError as e:
                if e:
                    print ('Error "%s" in adding secure policy to bucket %s' % (e, bucket))
                    text_output_array.append("Error ")
                    text_output_array.append(e)
                    text_output_array.append(" in adding secure bucket_policy to bucket ")
                    text_output_array.append(bucket)
                    text_output_array.append("\n")
                    sendEvent(text_output_array,SNS_TOPIC_ARN)
    except botocore.exceptions.ClientError as e:
         if e:
             s3_client.put_bucket_policy(Bucket=bucket,Policy=str_secure_bucket_policy)
             print ('Fixed bucket %s' % bucket)
             text_output_array.append("Added secure bucket_policy to bucket: ")
             text_output_array.append(bucket)
             text_output_array.append("\n")
             sendEvent(text_output_array,SNS_TOPIC_ARN)
