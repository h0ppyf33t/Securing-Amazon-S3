# s3-hardening
A Python (to be used in a AWS Lambda) project to harden the security posture of an AWS S3 bucket.

This project is meant to be implemented in a Lambda function which could take CloudTrail events such as 'CreateBucket' and 'PutBucketPolicy' as triggers or simply scheduled to run by a Cron expression.

[How to create a Cloudwatch Event CloudTrail rule](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/Create-CloudWatch-Events-CloudTrail-Rule.html)

[How to create a CloudWatch event rule](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/Create-CloudWatch-Events-Scheduled-Rule.html)

As we know all AWS S3 buckets are globally accessible via this endpoint http://<bucket_name>.s3.amazonaws.com. This is great and very easy to use but, not entirely secure as is. There are a few things you need enabled or tweaked to ensure whatever you put in your bucket is safe and secure to r/w.

Here's what this project helps you automate:
* Enable SSE (Server Side Encryption) for your bucket so data at rest are encrypted.
* Adds a bucket policy to deny all non-https traffic to ensure data in transit is secure.
* Enables bucket logging to ensure there is an audit trail to tract bucket access information.
