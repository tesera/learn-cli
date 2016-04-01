#!/usr/bin/env python
"""
Usage:
    learn varsel (--xy-data <file> --config <file>) [--yvar <string> --iteration <solutions:x-min:x-max> --criteria <string> --output <dir>]
    learn lda (--xy-data <file> --config <file>) [--yvar <string> --output <dir>]
    learn discrat (--xy-data <file> --x-data <file> --dfunct <file> --idf <file> --varset <int>) [--yvar <string> --output <dir>]

Options:
    --xy-data <file>  The path to the XY reference CSV file. Can be an S3://... path.
    --x-data <file>  The path to the X filtered data CSV file. Can be an S3://... path.
    --config <file>  Variable selection file. Can be an S3://... path. [default: ./config.csv]
    --yvar <string>  Class variable name: CLASS5, CLPRDP [default: Y].
    --iteration <string>  Iteration specific arguments for variable selection. <solutions:x-min:x-max> [default: 10:1:10]
    --criteria <string>  Set the criteria to be applied for variables selection: ccr12, Wilkes, xi2, zeta2 [default: xi2].
    --dfunct <file>  The path to the lda dfunct file to use for the discriminant rating.
    --idf <file>  The path to the IDF Curves file to use for the discriminant rating.
    --varset <int>  The ID of the varset to use for the discriminant rating.
    --output <dir>  Output folder. [default: ./]
    -h --help  Show help.

Examples:
    learn varsel --xy-data ./folder/xy_reference.csv --config ./folder/xvar_sel.csv --output ./output/varsel --iteration 10:1:10
    learn varsel --xy-data s3://bucket/xy_reference.csv --config s3://bucket/xvar_sel.csv --output s3://bucket/varsel --iteration 10:1:10
    learn lda --xy-data ./folder/xy_reference.csv --config ./folder/xvar_sel.csv --output./output/varsel
    learn lda --xy-data s3://bucket/xy_reference.csv --config s3://bucket/xvar_sel.csv --output s3://bucket/varsel
    learn discrat --xy-data ./folder/xy_reference.csv --x-data ./folder/x_filtered.csv --dfunct ./folder/dfunct.csv --idf ./folder/idf.csv --varset 18 --output ./output/varsel
    learn discrat --xy-data s3://bucket/xy_reference.csv --x-data s3://bucket/x_filtered.csv --dfunct s3://bucket/dfunct.csv --idf s3://bucket/idf.csv --varset 18 --output s3://bucket/varsel
"""

import os
import sys
import shutil
from urlparse import urlparse
import tempfile
from signal import *
import logging

import boto3
from docopt import docopt
from schema import Schema, And, Or, SchemaError, Optional

from clients.varselect import VarSelect
from clients.analyze import Analyze
from clients.discrating import Discrating

logger = logging.getLogger('pylearn')

def is_s3_url(url):
    return urlparse(url).scheme == 's3'

def cli():
    args = docopt(__doc__)

    # schema = Schema({
    #     'varsel': bool
    #     'lda': bool,
    #     'discrat': bool
    #     '--xy-data': Or(os.path.isfile, is_s3_url, error='<xy_reference_csv> should exist and be readable.'),
    #     '--x-data': Or(os.path.isfile, is_s3_url, error='<x_filtered_csv> should exist and be readable.'),
    #     '--config': And(Or(args['varsel'], args['lda']), Or(os.path.isfile, is_s3_url)), error='--config should exist and be readable.'),
    #     '--dfunct': Or(os.path.isfile, is_s3_url, error='--config should exist and be readable.'),
    #     '--idf': Or(os.path.isfile, is_s3_url, error='--config should exist and be readable.'),
    #     '--output': Or(os.path.exists, is_s3_url,  error='--output should exist and be writable.'),
    #     '--yvar': And(str, len),
    #     '--iteration': And(str, len),
    #     '--criteria': And(str, len),
    #     Optional('--help'): bool,
    # })

    # args = schema.validate(args)

    outdir = args['--output']
    outdir_url = urlparse(outdir)
    isS3Data = outdir_url.scheme == 's3'
    args['--output'] = tmp = tempfile.mkdtemp('learn-cli')
    args['--nSolutions'], args['--minNvar'], args['--maxNvar'] = args['--iteration'].split(':')

    if args['varsel']:
        command = 'varsel'
    elif args['lda']:
        command = 'lda'
    elif args['discrat']:
        command = 'discrat'

    clients = {
        'varsel': VarSelect,
        'lda': Analyze,
        'discrat': Discrating
    }
    files = {
        'varsel': [args['--xy-data'], args['--config']],
        'lda': [args['--xy-data'], args['--config']],
        'discrat': [args['--xy-data'], args['--x-data'], args['--dfunct'], args['--idf']]
    }
    files = files[command]


    if (isS3Data) :
        logger.info("copying s3 data files locally")
        try:
            s3_client = boto3.client('s3')
            for filepath in files:
                logger.info("copying %s from S3" % filepath)
                url = urlparse(filepath)
                file_path = os.path.join(tmp, filepath.split('/')[-1])
                s3_client.download_file(url.netloc, url.path.strip('/'), file_path)
                args[args.keys()[args.values().index(filepath)]] = file_path
        except Exception as e:
            logger.error("error copying data from s3: %s %s" % command, e)
            exit(e)
    else :
        for filepath in files:
            shutil.copy(filepath, tmp)

    # rename the passed in filenames to the legacy filenames jic they where hardcoded
    legacy_config = 'XVARSELV1.csv' if command is 'varsel' else 'XVARSELV.csv'

    legacy = {
        '--xy-data': os.path.join(tmp, 'ANALYSIS.csv'),
        '--config': os.path.join(tmp, legacy_config)
    }

    if command in ['varsel', 'lda']:
        os.rename(os.path.join(tmp, os.path.basename(args['--config'])), legacy['--config'])
        args['--config'] = legacy['--config']

    os.rename(os.path.join(tmp, os.path.basename(args['--xy-data'])), legacy['--xy-data'])
    args['--xy-data'] = legacy['--xy-data']

    try:
        args['--output'] = args['--output'].rstrip('/') + '/';

        client = clients[command]()
        client.run(args)

        if(isS3Data):
            logger.info("Copying results to s3 @ %s%s", outdir_url.netloc, outdir_url.path)
            for outfile in os.listdir(tmp):
                up = ("%s/%s" % (outdir_url.path, outfile)).strip('/')
                outfile = ("%s/%s" % (tmp, outfile))
                s3_client.upload_file(outfile, outdir_url.netloc, up.strip('/'))
        else:
            logger.info("Copying results to %s", outdir)
            for outfile in os.listdir(tmp):
                shutil.copy(os.path.join(tmp, outfile), os.path.join(outdir, outfile))

        exit(0)

    except SchemaError as e:
        logger.error("error running client %s with error %s", command, e)
        exit(e)
