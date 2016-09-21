import os
import sys
import logging
import pandas as pd

from pylearn.discrating import predict


logger = logging.getLogger('pylearn')


class Discrating(object):

    def __init__(self):
        logger.info("running dicsriminant ratings...")

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
