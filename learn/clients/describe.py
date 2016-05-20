import os
import logging
import pandas as pd
import prelurn


logger = logging.getLogger('describe')

class Describe(object):

    def __init__(self):
        pass

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
