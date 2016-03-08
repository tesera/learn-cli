#!/usr/bin/env python
"""
Usage:
    learn varsel [<xy_reference_csv>] [options]
    learn lda [<xy_reference_csv>] [options]

Arguments:
    <xy_reference_csv> The path to the XY reference CSV file. Can be an S3://... path.

Options:
    -h --help  Show help.
    -c <file>, --config <file>  Variable selection file. Can be an S3://... path. [default: ./config.csv]
    -o <dir>, --output <dir>  Output folder. [default: ./]
    --yvar <string>  Class variable name: CLASS5, CLPRDP [default: Y].
    --iteration <string>  Iteration specific arguments for variable selection. <solutions:x-min:x-max> [default: 10:1:10]
    --criteria <string>  Set the criteria to be applied for variables selection: ccr12, Wilkes, xi2, zeta2 [default: xi2].

Examples:
    learn varsel
    learn varsel ./myfolder/xy_reference.csv -x ./myfolder/xvar_sel.csv -o ./output/varsel --iteration 10:1:10
    learn varsel s3://my-bucket/xy_reference.csv -x s3://my-bucket/xvar_sel.csv -o s3://my-bucket/varsel --iteration 10:1:10
    learn lda
    learn lda ./myfolder/xy_reference.csv -x ./myfolder/xvar_sel.csv -o ./output/varsel
    learn lda s3://my-bucket/xy_reference.csv -x s3://my-bucket/xvar_sel.csv -o s3://my-bucket/varsel
"""

import os
import sys
import shutil
from urlparse import urlparse
import tempfile
from signal import *

import boto3
from docopt import docopt
from schema import Schema, And, Or, SchemaError, Optional

from clients.varselect import VarSelect
from clients.analyze import Analyze

def cli():
    args = docopt(__doc__)
    schema = Schema({
        Optional('varsel'): bool,
        Optional('lda'): bool,
        '<xy_reference_csv>': And(os.path.isfile, error='<xy_reference_csv> should exist and be readable.'),
        '--config': And(os.path.isfile, error='--config should exist and be readable.'),
        '--output': And(os.path.exists, error='--output should exist and be writable.'),
        '--yvar': And(str, len),
        '--iteration': And(str, len),
        '--criteria': And(str, len),
        Optional('--help'): bool,
    })

    args = schema.validate(args)

    outdir = args['--output']
    outdir_url = urlparse(outdir)
    isS3Data = outdir_url.scheme == 's3'
    args['--output'] = tmp = tempfile.mkdtemp('learn-cli')
    args['--nSolutions'], args['--minNvar'], args['--maxNvar'] = args['--iteration'].split(':')

    command = 'varsel' if args['varsel'] else 'lda'
    clients = {
        'varsel': VarSelect,
        'lda': Analyze
    }

    # prep the data files
    if (isS3Data) :
        try:
            s3_client = boto3.client('s3')
            for key in ['<xy_reference_csv>', '--config']:
                url = urlparse(args[key])
                dl = tempdir + '/' + args[key].split('/')[-1]
                s3_client.download_file(url.netloc, url.path.strip('/'), dl)
                args[key] = dl
        except Exception as e:
            exit(e)
    else :
        shutil.copy(args['<xy_reference_csv>'], tmp)
        shutil.copy(args['--config'], tmp)

    # here we rename the passed in filenames to the legacy filenames jic they where hardcoded
    legacy_config = 'XVARSELV1.csv' if command is 'varsel' else 'XVARSELV.csv'
    legacy = {
        '<xy_reference_csv>': os.path.join(tmp, 'ANALYSIS.csv'),
        '--config': os.path.join(tmp, legacy_config)
    }
    os.rename(os.path.join(tmp, os.path.basename(args['<xy_reference_csv>'])), legacy['<xy_reference_csv>'])
    os.rename(os.path.join(tmp, os.path.basename(args['--config'])), legacy['--config'])
    args['<xy_reference_csv>'] = legacy['<xy_reference_csv>']
    args['--config'] = legacy['--config']

    # start the process
    try:
        args['--output'] = args['--output'].rstrip('/') + '/';
        args['WORKINGDIR'] = os.getcwd().rstrip('/').replace('/bin', '') + '/'

        client = clients[command]()
        client.run(args)

        if(isS3Data):
            print "Copying results to %s%s", outdir_url.netloc, outdir_url.path
            for outfile in os.listdir(tmp):
                up = ("%s/%s" % (outdir_url.path, outfile)).strip('/')
                outfile = ("%s/%s" % (tmp, outfile))
                s3_client.upload_file(outfile, outdir_url.netloc, up.strip('/'))
        else:
            print "Copying results to %s" % outdir
            for outfile in os.listdir(tmp):
                shutil.copy(os.path.join(tmp, outfile), os.path.join(outdir, outfile))

        exit(0)

    except SchemaError as e:
        exit(e)
