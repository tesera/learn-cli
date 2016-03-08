#!/usr/bin/env python
"""
Usage:
    learn <operation> <datafile> <variablesfile> <outputdir> [options]

Arguments:
    <operation> varsel | lda
    <datafile>  Input file, local or S3 in format s3://bucket/path/filename.csv.
    <variablesfile>  File containing variable selections, local or S3 in format s3://bucket/path/filename.csv.
    <outputdir>  Directory to write results out too.

Options:
    --classVariableName=<string>  Class variable name: CLASS5, CLPRDP [default: CLPRDP].
    --excludeRowValue=<int>  Variable value to exclude rows from a dataset [default: -1].
    --excludeRowVarName=<string>  Variable name to exclude rows from a dataset [default: SORTGRP].
    --xVarSelectCriteria=<string>  Variable indicator value [default: X].
    --minNvar=<int>  Minimum number of variables to select [default: 1].
    --maxNvar=<int>  Maximum number of variables to select [default: 20].
    --nSolutions=<int>  Number of iterations to be applied [default: 10].
    --criteria=<string>  Set the criteria to be applied for variables selection: ccr12, Wilkes xi2 zeta2 [default: xi2].
    --tempDir=<string>  Use this temp directory instead of generating one.
    --priorDistribution=<string>  TODO: Describe [default: SAMPLE]
    --classNames=<string>  TODO: Describe. [default: CLPRDP]
"""

import os
import sys
import shutil
from urlparse import urlparse
import tempfile
from signal import *

from docopt import docopt
from schema import Schema, And, Or, Use, SchemaError, Optional
import boto3

from rpy2.robjects.packages import importr

from clients.varselect import VarSelect
from clients.analyze import Analyze

def cli():
    args = docopt(__doc__)
    flog = importr('futile.logger')
    clients = {
        'varsel': VarSelect,
        'lda': Analyze
    }

    schema = Schema({
        '<operation>': And(str, len),
        '<datafile>': And(os.path.isfile, error='<datafile> should exist and be readable.'),
        '<variablesfile>': And(os.path.isfile, error='<variablesfile> should exist and be readable.'),
        '<outputdir>': And(os.path.exists, error='<outputdir> should exist and be writable.'),
        Optional('--classVariableName'): And(str, len),
        Optional('--excludeRowValue'): And(str, len),
        Optional('--excludeRowVarName'): And(str, len),
        Optional('--xVarSelectCriteria'): And(str, len),
        Optional('--minNvar'): And(str, len),
        Optional('--maxNvar'): And(str, len),
        Optional('--nSolutions'): And(str, len),
        Optional('--criteria'): And(str, len),
        Optional('--tempDir'): Or(None, And(str, len)),
        Optional('--priorDistribution'): Or(None, And(str, len)),
        Optional('--classNames'): Or(None, And(str, len))
    })

    operation = args['<operation>']
    outdir = args['<outputdir>']
    outdir_url = urlparse(outdir)
    isS3Data = outdir_url.scheme == 's3'
    tmp = args['--tempDir'] if args['--tempDir'] else tempfile.mkdtemp('features')

    args['<outputdir>'] = tempdir = tmp

    # prep the data files
    if (isS3Data) :
        try:
            s3_client = boto3.client('s3')
            for key in ['<datafile>', '<variablesfile>']:
                url = urlparse(args[key])
                dl = tempdir + '/' + args[key].split('/')[-1]
                s3_client.download_file(url.netloc, url.path.strip('/'), dl)
                args[key] = dl
        except Exception as e:
            exit(e)
    else :
        shutil.copy(args['<datafile>'], tmp)
        shutil.copy(args['<variablesfile>'], tmp)

    # start the process
    try:
        args = schema.validate(args)
        args['<outputdir>'] = args['<outputdir>'].rstrip('/') + '/';
        args['WORKINGDIR'] = os.getcwd().rstrip('/').replace('/bin', '') + '/'

        client = clients[operation]()
        client.run(args)

        if(isS3Data):
            flog.flog_info("Copying results to %s%s", outdir_url.netloc, outdir_url.path)
            for outfile in os.listdir(tempdir):
                up = ("%s/%s" % (outdir_url.path, outfile)).strip('/')
                outfile = ("%s/%s" % (tempdir, outfile))
                s3_client.upload_file(outfile, outdir_url.netloc, up.strip('/'))
        else:
            flog.flog_info("Copying results to %s", outdir)
            shutil.copytree(tempdir, outdir)

        exit(0)

    except SchemaError as e:
        exit(e)
