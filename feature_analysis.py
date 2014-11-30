"""
Feature Analyzer

Usage:
  feature_analysis.py [--cache_file FILE]

Options:
  --cache_file FILE   Cache filename e.g. FooFeatureExtractor.json
"""

import json
import sys

from docopt  import docopt

arguments = docopt(__doc__, version='0.0.1')
filename = arguments['--cache_file']

with open(filename) as f:
    data = json.loads(f.read())
    feature_dict = {}
    counts = []
    movie_count = 0
    for movie_id, features in data.iteritems():
        #features = features['features']
        if len(features.keys()) == 0:
            continue
        movie_count += 1
        for cast in features.keys():
            feature_dict[cast] = 1 + feature_dict.get(cast, 0)
        counts.append(len(features.keys()))
    print "%d movies" % movie_count
    print "%d unique features" % len(feature_dict.keys())
    print "%d average features per movie" % (
        sum(counts) / float(movie_count))
