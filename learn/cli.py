"""
Usage:
    learn describe (--xy-data <file>) [--quantile-type <string> --format <string> --output <dir>]
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
    --format <string>  Output format: json or csv. [default: json]
    --quantile-type <string>  Quantiles: decile or quartile. [default: decile]
    --output <dir>  Output folder. [default: ./]
    -h --help  Show help.

Examples:
    learn describe --xy-data ./folder/xy_reference.csv --quantile-type decile --format json --output ./output/describe
    learn describe --xy-data s3://bucket/xy_reference.csv --quantile-type decile --format json --output s3://bucket/describe
    learn varsel --xy-data ./folder/xy_reference.csv --config ./folder/xvar_sel.csv --output ./output/varsel --iteration 10:1:10
    learn varsel --xy-data s3://bucket/xy_reference.csv --config s3://bucket/xvar_sel.csv --output s3://bucket/varsel --iteration 10:1:10
    learn lda --xy-data ./folder/xy_reference.csv --config ./folder/xvar_sel.csv --output./output/varsel
    learn lda --xy-data s3://bucket/xy_reference.csv --config s3://bucket/xvar_sel.csv --output s3://bucket/varsel
    learn discrat --xy-data ./folder/xy_reference.csv --x-data ./folder/x_filtered.csv --dfunct ./folder/dfunct.csv --idf ./folder/idf.csv --varset 18 --output ./output/varsel
    learn discrat --xy-data s3://bucket/xy_reference.csv --x-data s3://bucket/x_filtered.csv --dfunct s3://bucket/dfunct.csv --idf s3://bucket/idf.csv --varset 18 --output s3://bucket/varsel
"""

import os
import shutil
from urlparse import urlparse
import tempfile
import logging

import boto3
from docopt import docopt

from clients.varselect import VarSelect
from clients.analyze import Analyze
from clients.discrating import Discrating
from clients.describe import Describe


logger = logging.getLogger('pylearn')

def cli():
    args = docopt(__doc__)

    clients = {
        'describe': Describe,
        'varsel': VarSelect,
        'lda': Analyze,
        'discrat': Discrating,
    }
    files = {
        'describe': [args['--xy-data']],
        'varsel': [args['--xy-data'], args['--config']],
        'lda': [args['--xy-data'], args['--config']],
        'discrat': [args['--xy-data'], args['--x-data'], args['--dfunct'], args['--idf']],
    }

    outdir = args['--output']
    tmpdir = tempfile.mkdtemp('learn-cli')
    args['--output'] = tmpdir.rstrip('/') + '/'

    s3bucket = None
    outdir_url = urlparse(outdir)
    if outdir_url.scheme == 's3':
        s3bucket = outdir_url.netloc
        s3prefix = outdir_url.path.strip('/')

    if args['describe']:
        command = 'describe'
    elif args['varsel']:
        command = 'varsel'
    elif args['lda']:
        command = 'lda'
    elif args['discrat']:
        command = 'discrat'

    infiles = files[command]
    if s3bucket:
        logger.info("copying s3 data files locally")
        try:
            s3_client = boto3.client('s3')
            for infile in infiles:
                logger.info("copying %s from S3", infile)
                url = urlparse(infile)
                file_path = os.path.join(tmpdir, infile.split('/')[-1])
                s3_client.download_file(url.netloc, url.path.strip('/'), file_path)
                args[args.keys()[args.values().index(infile)]] = file_path
        except Exception as e:
            logger.error("error copying data from s3: %s %s", command, e)
            exit(1)
    else:
        for infile in infiles:
            shutil.copy(infile, tmpdir)

    # make a list of the input filenames passsed in so we don't copy them to the output
    infilenames = [os.path.basename(f) for f in os.listdir(tmpdir)]
    log_files = ['pylearn.log'] if command in ['describe', 'discrat'] \
                else ['pylearn.log', 'rlearn.log']

    try:
        client = clients[command]()
        client.run(args)
        if s3bucket:
            copy_output_files_to_s3(s3_client, s3bucket, s3prefix,
                                    tmpdir, infilenames, log_files)
        else:
            copy_output_files_to_folder(outdir, tmpdir, infilenames)

        exit(0)

    except Exception as e:
        logging.error(e)
        if s3bucket:
            copy_output_files_to_s3(s3_client, s3bucket, s3prefix,
                                    tmpdir, infilenames, log_files)
        else:
            copy_output_files_to_folder(outdir, tmpdir, infilenames)

        exit(1)

def copy_output_files_to_s3(s3client, s3bucket, s3prefix, in_dir,
                            exclude_files, cwd_files):
    """Copy files to s3 bucket

    :param s3bucket: s3 bucket URI, no trailing slash
    :param s3prefix: folder, no leading slash
    :param in_dir: directory from which to copy files
    :param exclude: paths to exclude relative to dir
    :cwd_files: additional files to copy from the working directory

    """
    logger.info("Copying results to s3 bucket %s to prefix %s", s3bucket, s3prefix)
    for filename in os.listdir(in_dir):
        if filename in exclude_files:
            continue
        filepath = os.path.join(in_dir, filename)
        key = "%s/%s" % (s3prefix, filename)
        logger.info("Copying %s to %s", filepath, key)
        s3client.upload_file(filepath, s3bucket, key)

    for filename in cwd_files:
        logfile_path = os.path.join(os.getcwd(), filename)
        key = "%s/%s" % (s3prefix, filename)
        logger.info("Copying logfile %s to %s", filename, key)
        if os.path.exists(logfile_path):
            s3client.upload_file(logfile_path, s3bucket, key)
        else:
            logger.warning('File %s cannot be copied to s3; file does not exist',
                           logfile_path)


def copy_output_files_to_folder(destination, in_dir, exclude_files):
    """Copy files to s3 bucket

    :param destination: destination directory for files
    :param in_dir: directory from which to copy files
    :param exclude_files: paths to exclude relative to dir

    """
    logger.info("Copying results to %s", destination)

    if not os.path.exists(destination):
        os.makedirs(destination)

    for outfile in os.listdir(in_dir):
        if outfile in exclude_files:
            continue
        shutil.copy(os.path.join(in_dir, outfile), os.path.join(destination, outfile))



