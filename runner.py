#!/usr/bin/env python

import subprocess
import sys
import boto3
import time

mrat_args = sys.argv
mrat_args.pop(0)
log_stream_name = str(int(time.time())) 
mrat_args.pop(0)
log_group_name = '/aws/mrat/variable-selection'

cw_client = boto3.client('logs', 'us-east-1')
cw_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
response = {}

def log(line):
	global response
	if 'nextSequenceToken' in response:
		new_response = cw_client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[{'timestamp': int(time.time())*1000, 'message': line}], sequenceToken=response['nextSequenceToken'])
	else:
		new_response = cw_client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[{'timestamp': int(time.time())*1000, 'message': line}])

	print(new_response)
	response = new_response

proc = subprocess.Popen(['python','mrat.py'] + mrat_args, stdout=subprocess.PIPE)
while True:
	line = proc.stdout.readline()
	if line != '':
		log(line)
	else:
		break