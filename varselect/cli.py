#!/usr/bin/env python
"""varselect

Usage:
  varselect LVIFILENAME XVARSELECTFILENAME OUTDIR
  varselect LVIFILENAME XVARSELECTFILENAME OUTDIR \
 [--classVariableName=<string>] \
 [--excludeRowValue=<int>] \
 [--excludeRowVarName=<string>] \
 [--xVarSelectCriteria=<string>] \
 [--minNvar=<int>] \
 [--maxNvar=<int>] \
 [--nSolutions=<int>] \
 [--criteria=<int>] \
 [--tempDir=<string>]


Arguments:
  LVIFILENAME  Input file, local or S3 in format s3://bucket/path/filename.csv.
  XVARSELECTFILENAME  File containing variable selections, local or S3 in format s3://bucket/path/filename.csv.
  OUTDIR  Directory to write results out too.

Options:
  -h --Help  Show this screen.
  --classVariableName=<string>  Class variable name: CLASS5, CLPRDP [default: CLASS5].
  --excludeRowValue=<int>  Variable value to exclude rows from a dataset [default: -1].
  --excludeRowVarName=<string>  Variable name to exclude rows from a dataset [default: SORTGRP].
  --xVarSelectCriteria=<string>  Variable indicator value [default: X].
  --minNvar=<int>  Minimum number of variables to select [default: 1].
  --maxNvar=<int>  Maximum number of variables to select [default: 20].
  --nSolutions=<int>  Number of iterations to be applied [default: 20].
  --criteria=<string>  Set the criteria to be applied for variables selection: ccr12, Wilkes xi2 zeta2 [default: xi2].
  --tempDir=<string>  Use this temp directory instead of generating one.

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

# from varselect import Runner

# determine if required
# import atexit
# import pdb # ?
# import imp # ?
# import pip # something better?

from libvariableselection.count_xvar_in_xvarsel import CountXVarInXvarSel
from libvariableselection.test_extract_rvariable_combos import ExtractRVariableCombos
from libvariableselection.rank_var import RankVar
from libvariableselection.remove_highcorvar_from_xvarsel import RemoveHighCorVarFromXVarSel

#flog.flog_appender(flog.appender_file('varselect.log'))

def cli():
    args = docopt(__doc__)
    schema = Schema({
        'LVIFILENAME': And(os.path.isfile, error='LVIFILENAME should exist and be readable.'),
        'XVARSELECTFILENAME': And(os.path.isfile, error='XVARSELECTFILENAME should exist and be readable.'),
        'OUTDIR': And(os.path.exists, error='OUTDIR should exist and be writable.'),
        Optional('--classVariableName'): And(str, len),
        Optional('--excludeRowValue'): And(str, len),
        Optional('--excludeRowVarName'): And(str, len),
        Optional('--xVarSelectCriteria'): And(str, len),
        Optional('--minNvar'): And(str, len),
        Optional('--maxNvar'): And(str, len),
        Optional('--nSolutions'): And(str, len),
        Optional('--criteria'): And(str, len),
        Optional('--tempDir'): Or(None, And(str, len))
    })

    s3_client = boto3.client('s3')
    outdir = args['OUTDIR']
    tmp = tempfile.mkdtemp('varselect')

    if args['--tempDir'] != None:
        tmp = args['--tempDir']

    args['OUTDIR'] = tempdir = tmp

    try:
        for key in ['LVIFILENAME', 'XVARSELECTFILENAME']:
            url = urlparse(args[key])
            if url.scheme == 's3':
                dl = tempdir + '/' + args[key].split('/')[-1]
                s3_client.download_file(url.netloc, url.path.strip('/'), dl)
                args[key] = dl
    except Exception as e:
            exit(e)

    args['LVIFILENAME'] = os.path.abspath(args['LVIFILENAME'])
    args['XVARSELECTFILENAME'] = os.path.abspath(args['XVARSELECTFILENAME'])
    args['OUTDIR'] = os.path.abspath(args['OUTDIR'])

    print 'all good til here'
    print str(args)

    try:
        args = schema.validate(args)
        args['OUTDIR'] = args['OUTDIR'].rstrip('/') + '/';
        args['WORKINGDIR'] = os.getcwd().rstrip('/').replace('/bin', '') + '/'

        runner = Runner()
        runner.variable_selection(args)

        outdir_url = urlparse(outdir)

        if(outdir_url.scheme == 's3'):
            flog.flog_info("Copying results to %s%s", outdir_url.netloc, outdir_url.path)
            for outfile in os.listdir(tempdir):
                up = ("%s/%s" % (outdir_url.path, outfile)).strip('/')
                outfile = ("%s/%s" % (tempdir, outfile))
                s3_client.upload_file(outfile, outdir_url.netloc, up.strip('/'))
        else:
            flog.flog_info("Copying results to %s", outdir)
            if not os.path.exists(outdir):
                os.makedirs(outdir)

            for outfile in os.listdir(tempdir):
                up = ("%s/%s" % (outdir, outfile))
                outfile = ("%s/%s" % (tempdir, outfile))
                shutil.copy(outfile, up)

        exit(0)

    except SchemaError as e:
        exit(e)
