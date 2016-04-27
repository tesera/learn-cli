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
from urlparse import urlparse, urljoin
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

def cli():
    args = docopt(__doc__)

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

    outdir = args['--output']
    tmpdir = tempfile.mkdtemp('learn-cli')
    args['--output'] = tmpdir.rstrip('/') + '/'

    s3bucket = None
    outdir_url = urlparse(outdir)
    if outdir_url.scheme == 's3':
        s3bucket = outdir_url.netloc
        s3prefix = outdir_url.path.strip('/')

    if args['varsel']:
        command = 'varsel'
    elif args['lda']:
        command = 'lda'
    elif args['discrat']:
        command = 'discrat'

    infiles = files[command]

    # copy input files to tmpdir folder for processing
    if (s3bucket) :
        logger.info("copying s3 data files locally")
        try:
            s3_client = boto3.client('s3')
            for infile in infiles:
                logger.info("copying %s from S3" % infile)
                url = urlparse(infile)
                file_path = os.path.join(tmpdir, infile.split('/')[-1])
                s3_client.download_file(url.netloc, url.path.strip('/'), file_path)
                args[args.keys()[args.values().index(infile)]] = file_path
        except Exception as e:
            # logger.error("error copying data from s3: %s %s", command, e)
            exit(e)
    else :
        for infile in infiles:
            shutil.copy(infile, tmpdir)

    # rename the passed in filenames to the legacy filenames jic they where hardcoded
    legacy_config = 'XVARSELV1.csv' if command is 'varsel' else 'XVARSELV.csv'

    legacy = {
        '--xy-data': os.path.join(tmpdir, 'ANALYSIS.csv'),
        '--config': os.path.join(tmpdir, legacy_config)
    }

    if command in ['varsel', 'lda']:
        os.rename(os.path.join(tmpdir, os.path.basename(args['--config'])), legacy['--config'])
        args['--config'] = legacy['--config']

    os.rename(os.path.join(tmpdir, os.path.basename(args['--xy-data'])), legacy['--xy-data'])
    args['--xy-data'] = legacy['--xy-data']

    # make a list of the input filenames passsed in so we don't copy them to the output
    infilenames = [os.path.basename(f) for f in os.listdir(tmpdir)]

    try:

        # run the command client with the args
        client = clients[command]()
        client.run(args)

        # copy only output files to output dir
        if(s3bucket):
            logger.info("Copying results to s3 bucket %s to prefix %s", s3bucket, s3prefix)
            for filename in os.listdir(tmpdir):
                if filename not in infilenames:
                    filepath = os.path.join(tmpdir, filename)
                    key = "%s/%s" % (s3prefix, filename)
                    logger.info("Copying %s to %s", filepath, key)
                    s3_client.upload_file(filepath, s3bucket, key)

            for logfile in ['pylearn.log']:
                logfile_path = os.path.join(os.getcwd(), logfile)
                key = "%s/%s" % (s3prefix, logfile)
                logger.info("Copying logfile %s to %s", logfile, key)
                s3_client.upload_file(logfile_path, s3bucket, key)
        else:
            logger.info("Copying results to %s", outdir)

            if not os.path.exists(outdir):
                os.makedirs(outdir)

            for outfile in os.listdir(tmpdir):
                if outfile not in infilenames:
                    shutil.copy(os.path.join(tmpdir, outfile), os.path.join(outdir, outfile))

        exit(0)

    except Exception as e:
        logging.error(e)
        exit(1)
