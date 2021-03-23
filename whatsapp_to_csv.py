"""
whatsapp_to_csv: Convert a whatsapp .txt file to a pandas-compatible .csv

Usage:
    whatsapp_to_csv <input_file> <output_file> [--params-file=params.yaml]

Options:
    --params-file=params.yaml   YAML file to take params from [default: params.yaml]
"""

import pandas as pd 
import yaml
import sys 
import re 
from docopt import docopt
import logging as log 

def main(args):
    
    # get parameters for this run
    params = yaml.safe_load(open(args['--params-file']))['whatsapp_to_csv']

    log.basicConfig(level=params['log_level'])
    log.debug(f'Arguments are: {args}')
    log.info(f'Parameters:\n{yaml.safe_dump(params)}')

    # open the whatsapp file
    with open(args['<input_file>'], encoding='utf8') as f:
        wa = f.read()

    # Perform character substitution for gremlin unicode characters
    wa = wa.replace('\u200e', '') # strange left-to-right character
    wa = wa.replace("\u201c", '"') # open quote character
    wa = wa.replace("\u201d", '"') # close quote character
    wa = wa.replace("\u2019", "'") # apostrophe character
    wa = wa.replace("\u2018", "'") # another apostrophe
    wa = wa.replace("\u2013", "-") # dash
    wa = wa.replace("\u00A0", " ") # non breaking space
    wa = wa.replace("\u202C", "") # more non-space character
    
    regexp_str = r'([0-9]+/[0-9]+/[0-9]+), ([0-9]+:[0-9]+:[0-9]+)\](.*?):(.*?)\['
    regexp = re.compile(regexp_str, re.MULTILINE + re.DOTALL)

    matches = regexp.findall(wa)
    
    log.info(f'Number of regexp matches: {len(matches)}')

    df = pd.DataFrame(matches, columns=['date','time','author','msg'])
    df.index.name = "msgid"

    # ignore the first several lines as they are garbage
    df = df.iloc[4:,:]
    # Trim the trailing newline
    df.loc[:,'msg'] = df.msg.str[:-1]
    df.reset_index(drop=True)
    
    # Write the csv
    df.to_csv(args['<output_file>'])

if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
