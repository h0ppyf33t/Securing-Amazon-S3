# Its generally a good practive to have an aggregate bucket to store all access logs.

import json
import boto3
import botocore
from send_to_sns import *

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def bucket_logging(SNS_TOPIC_ARN,text_output_array):
    bucket_logging = []
    dict_enable_logging = {}

    # Just itretating through all the available buckets to find the aggregate bucket(s).
    # Trying to be as region specific as possible. Ignoring alb aggreate buckets. You get the idea.
    for bucket in s3.buckets.all():
      bucket=bucket.name
      if 'us-east-1' in bucket and 'access-log-storage-s3' in bucket and not 'alb' in bucket:
       us_east_1_access_bkt = bucket
      elif 'us-west-2' in bucket and 'access-log-storage-s3' in bucket and not 'alb' in bucket:
       us_west_2_access_bkt = bucket
      elif 'eu-east-2' in bucket and 'access-log-storage-s3' in bucket and not 'alb' in bucket:
       eu_east_2_access_bkt = bucket

	# Iterate through all the buckets available
    for bucket in s3.buckets.all():
       bucket=bucket.name
       try:
          bucket_logging = s3_client.get_bucket_logging(Bucket=bucket)
          # Check if logging is enabled and to the s3 storage bucket
          if 'LoggingEnabled' in bucket_logging:
           target_bucket = bucket_logging['LoggingEnabled']['TargetBucket']
           target_prefix = bucket_logging['LoggingEnabled']['TargetPrefix']
           # Prase the bucketlocation from ResponseMetadata.
           bucket_location = s3_client.head_bucket(Bucket=bucket)['ResponseMetadata']['HTTPHeaders']['x-amz-bucket-region']

           # Checking if the exising bucket logging policy writes logs only to the aggregate bucket.
           # TargetBucket = the aggreate bucket.
           # TargetPrefix = the name of the bucket.
           if (bucket_location == 'us-east-1' and us_east_1_access_bkt) and target_bucket!=us_east_1_access_bkt :
            target_bucket = us_east_1_access_bkt
            target_prefix = bucket
            dict_enable_logging= {'LoggingEnabled': {'TargetBucket': '%s' % target_bucket, 'TargetPrefix': '%s' % target_prefix }}
            s3_client.put_bucket_logging(Bucket=bucket,BucketLoggingStatus=dict_enable_logging)
            print('Fixed bucket logging for %s' % dict_enable_logging)
            text_output_array.append("Fixed bucket_logging for: ")
            text_output_array.append(bucket)
            text_output_array.append("\n")
            sendEvent(text_output_array,SNS_TOPIC_ARN)

           elif (bucket_location == 'us-west-2' and us_west_2_access_bkt) and target_bucket!=us_west_2_access_bkt:
            target_bucket = us_west_2_access_bkt
            target_prefix = bucket
            dict_enable_logging= {'LoggingEnabled': {'TargetBucket': '%s' % target_bucket, 'TargetPrefix': '%s' % target_prefix }}
            s3_client.put_bucket_logging(Bucket=bucket,BucketLoggingStatus=dict_enable_logging)
            print('Bucket logging enabled for %s' % dict_enable_logging)
            text_output_array.append("Fixed bucket_logging for: ")
            text_output_array.append(bucket)
            text_output_array.append("\n")
            sendEvent(text_output_array,SNS_TOPIC_ARN)

           elif (bucket_location == 'eu-east-2' and eu_east_2_access_bkt) and target_bucket!=eu_east_2_access_bkt:
            target_bucket = eu_east_2_access_bkt
            target_prefix = bucket
            dict_enable_logging= {'LoggingEnabled': {'TargetBucket': '%s' % target_bucket, 'TargetPrefix': '%s' % target_prefix }}
            s3_client.put_bucket_logging(Bucket=bucket,BucketLoggingStatus=dict_enable_logging)
            print('Bucket logging enabled for %s' % dict_enable_logging)
            text_output_array.append("Fixed bucket_logging for: ")
            text_output_array.append(bucket)
            text_output_array.append("\n")
            sendEvent(text_output_array,SNS_TOPIC_ARN)

           else:
            print ('Nothing to do for bucket: %s' % bucket)

          # If turned off. Enable bucket logging.
          else:
           bucket_location = s3_client.head_bucket(Bucket=bucket)['ResponseMetadata']['HTTPHeaders']['x-amz-bucket-region']
           if (bucket_location == 'us-east-1' and us_east_1_access_bkt):
            target_bucket = us_east_1_access_bkt
            target_prefix = bucket
            dict_enable_logging= {'LoggingEnabled': {'TargetBucket': '%s' % target_bucket, 'TargetPrefix': '%s' % target_prefix }}
            print('Logging was turned off. Enabled logging. Current logging status: %s' % dict_enable_logging)
            s3_client.put_bucket_logging(Bucket=bucket,BucketLoggingStatus=dict_enable_logging)
            text_output_array.append("Enabled bucket_logging for: ")
            text_output_array.append(bucket)
            text_output_array.append("\n")
            sendEvent(text_output_array,SNS_TOPIC_ARN)

           elif (bucket_location == 'us-west-2' and us_west_2_access_bkt):
            target_bucket = us_west_2_access_bkt
            target_prefix = bucket
            dict_enable_logging= {'LoggingEnabled': {'TargetBucket': '%s' % target_bucket, 'TargetPrefix': '%s' % target_prefix }}
            print('Logging was turned off. Enabled logging. Current logging status: %s' % dict_enable_logging)
            s3_client.put_bucket_logging(Bucket=bucket,BucketLoggingStatus=dict_enable_logging)
            text_output_array.append("Enabled bucket_logging for: ")
            text_output_array.append(bucket)
            text_output_array.append("\n")

           elif (bucket_location == 'eu-east-2' and eu_east_2_access_bkt):
            target_bucket = eu_east_2_access_bkt
            target_prefix = bucket
            dict_enable_logging= {'LoggingEnabled': {'TargetBucket': '%s' % target_bucket, 'TargetPrefix': '%s' % target_prefix }}
            print('Logging was turned off. Enabled logging. Current logging status: %s' % dict_enable_logging)
            s3_client.put_bucket_logging(Bucket=bucket,BucketLoggingStatus=dict_enable_logging)
            text_output_array.append("Enabled bucket_logging for: ")
            text_output_array.append(bucket)
            text_output_array.append("\n")
           else:
            print ('Nothing to do for bucket: %s' % bucket)

       except botocore.exceptions.ClientError as e:
           if e:
               print('Error %s in remediating bucket %s' % (e,bucket))
               text_output_array.append("Error ")
               text_output_array.append(e)
               text_output_array.append(" in fixing bucket ")
               text_output_array.append(bucket)
               text_output_array.append("\n")
