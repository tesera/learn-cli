import os
import sys
import logging
import pandas as pd
from schema import Schema, And, Or
from pylearn.discrating import predict

from learn.utils import is_s3_url

logger = logging.getLogger('pylearn')


class Discrating(object):

    def __init__(self):
        logger.info("running dicsriminant ratings...")

    @staticmethod
    def _validate(args):
        schema = Schema({
            '--xy-data': Or(
                os.path.isfile, is_s3_url,
                error='<--xy-data should exist and be readable.'),
            '--x-data': Or(
                os.path.isfile, is_s3_url,
                error='--x-data should exist and be readable.'),
            '--dfunct': Or(
                os.path.isfile, is_s3_url,
                error='--dfunct should exist and be readable.'),
            '--idf': Or(
                os.path.exists, is_s3_url,
                error='--idf should exist and be writable.'),
            '--output': Or(
                os.path.exists, is_s3_url,
                error='--output should exist and be writable.'),
            '--yvar': And(str, len),
        }, ignore_extra_keys=True)
        args = schema.validate(args)
        return args

    def run(self, args):
        varset = int(args['--varset'])
        dfunct = pd.read_csv(args['--dfunct'])

        # this is a hack to avoid handling this in pylearn right now in pylearn
        # an exception should be raised which we can catch when running predict
        if varset not in dfunct.VARSET3.unique():
            msg = "varset '%d' missing from dfunct" %varset
            logger.error(msg)
            sys.exit(msg)

        pargs = {
            'xy': pd.read_csv(args['--xy-data']),
            'x_filtered': pd.read_csv(args['--x-data']),
            'dfunct': dfunct,
            'varset': varset,
            'yvar': args['--yvar'],
            'idf': pd.read_csv(args['--idf']),
        }

        forecasts = predict(**pargs)

        forecasts.to_csv(os.path.join(args['--output'], 'forecasts.csv'))
