import os
import logging

import pandas as pd

from pylearn.ldanalysis.varset import get_param
from pylearn.discrating import predict

logger = logging.getLogger('pylearn')

class Discrating(object):

    def __init__(self):
        logger.info("running dicsriminant ratings...")

    def run(self, args):
        logger.info("exporting varset %s as dfunct..." % args['--varset'])
        dfunct = pd.read_csv(args['--dfunct'])
        param = get_param(dfunct, int(args['--varset']))

        pargs = {
            'xy': pd.read_csv(args['--xy-data']),
            'x_filtered': pd.read_csv(args['--x-data']),
            'param': param,
            'idf': pd.read_csv(args['--idf']),
        }

        logger.info("invoking predict...")
        forecasts = predict(**pargs)
        forecasts.to_csv(os.path.join(args['--output'], 'forecasts.csv'))
