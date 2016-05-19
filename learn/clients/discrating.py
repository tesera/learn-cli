import os
import logging

import pandas as pd

from pylearn.varset import get_param
from pylearn.discrating import predict

logger = logging.getLogger('pylearn')

class Discrating(object):

    def __init__(self):
        logger.info("running dicsriminant ratings...")

    def run(self, args):
        logger.info("invoking predict with varset: %s", args['--varset'])

        pargs = {
            'xy': pd.read_csv(args['--xy-data']),
            'x_filtered': pd.read_csv(args['--x-data']),
            'dfunct': pd.read_csv(args['--dfunct']),
            'varset': int(args['--varset']),
            'yvar': args['--yvar'],
            'idf': pd.read_csv(args['--idf']),
        }

        forecasts = predict(**pargs)

        forecasts.to_csv(os.path.join(args['--output'], 'forecasts.csv'))
