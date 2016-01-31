#!/usr/bin/env python

import subprocess
import sys
import boto3
import time
import uuid
import os
import tempfile
import shutil
from urlparse import urlparse

mrat_args = sys.argv
mrat_args.pop(0)
log_stream_name = mrat_args.pop(0)
outdir = mrat_args[2]
log_group_name = '/aws/mrat/variable-selection'
cw_client = boto3.client('logs', 'us-east-1')
s3_client = boto3.client('s3')

try:
	cw_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
except:
	# create new stream if repeat
    log_stream_name = str(uuid.uuid4())
    cw_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
response = {}

def log(line):
	global response
	global log_client

	if 'nextSequenceToken' in response:
		new_response = cw_client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[{'timestamp': int(time.time())*1000, 'message': line}], sequenceToken=response['nextSequenceToken'])
	else:
		new_response = cw_client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[{'timestamp': int(time.time())*1000, 'message': line}])
	response = new_response

	log_client.write(line)
	sys.stdout.write(line)

tmp = tempfile.mkdtemp('mrat')
mrat_args.append('--tempDir=' + tmp)
log_file = tmp + '/log.txt'
log_client = open(log_file, 'w+')
log_client.write(str(sys.argv))

proc = subprocess.Popen(['python','mrat.py'] + mrat_args, stdout=subprocess.PIPE)
while True:
	line = proc.stdout.readline()
	if line != '':
		log(line)
	else:
		# until every log is converted to flog
		log_client.close()
		outdir_url = urlparse(outdir)
		if(outdir_url.scheme == 's3'):
			up = ("%s/%s" % (outdir_url.path, 'log.txt')).strip('/')
			s3_client.upload_file(log_file, outdir_url.netloc, up.strip('/'))
		else:
			shutil.copy(log_file, outdir)
		break
