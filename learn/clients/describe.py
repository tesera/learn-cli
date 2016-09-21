import os
import logging
import pandas as pd
import prelurn
from schema import Schema, And, Or, Optional

from learn.utils import is_s3_url

logger = logging.getLogger('pylearn')

class Describe(object):

    def __init__(self):
        pass

    @staticmethod
    def _validate(args):
        schema = Schema({
            '--xy-data': Or(
                os.path.isfile, is_s3_url,
                error='<xy_reference_csv> should exist and be readable.'),
            Optional('--quantile-type'): And(
                str,
                lambda s: s in ('decile', 'quartile'),
                error='--config should exist and be readable.'),
            '--output': Or(
                os.path.exists, is_s3_url,
                error='--output should exist and be writable.'),
            Optional('--format'): And(str, lambda s: s in ('json', 'csv')),
        }, ignore_extra_keys=True)
        args = schema.validate(args)
        return args


    def run(self, args):
        logger.info('Running describe')

        data = pd.read_csv(args['--xy-data'])
        fmt = args['--format']
        quantile_type = args['--quantile-type']

        description = prelurn.describe(data, quantile_type=quantile_type)

        out_file_path = os.path.join(args['--output'], 'describe')
        if fmt == 'json':
            out_file_path += '.json'
            description.to_json(out_file_path, orient='columns')
        elif fmt == 'csv':
            out_file_path += '.csv'
            description.to_csv(out_file_path)
        else:
            raise ValueError('%s is invalid format', fmt)
