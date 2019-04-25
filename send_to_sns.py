import boto3
from botocore.exceptions import ClientError


def sendEvent(text_output_array,SNS_TOPIC_ARN):
	text_output_array.append("-------------------------\n")
	text_output_str = ''.join(text_output_array)
	sns = boto3.client('sns')

	response = sns.publish(
		TopicArn=SNS_TOPIC_ARN,
		Message=text_output_str,
		Subject='S3AutoRemediationLog',
		MessageStructure='string'
		)

	status_code = response['ResponseMetadata']['HTTPStatusCode']
	if status_code > 400:
		print("SNS message failed to send!")
		print(str(response))
	else:
		print("SNS message posted successfully")