# -*- coding: utf-8 -*-
"""
Feature Creator

Usage:
  feature_creator.py [options]

Options:
  -h --help             Show this screen.
  --version             Version number.
  --verbose             Print output to STDOUT
"""

import inspect
import logging
import os
import sys

from docopt  import docopt

from cache import Cache
from session import session

from movie_filter import MovieFilter
import models
import feature_extractors
from models.info_type import RATING_ID
from helpers import encode


class FeatureCreator(object):
    FEATURES_PATH = os.path.join('data', 'features.json')
    LOGGING_FORMAT = '%(levelname)s %(asctime)s: %(message)s'

    def __init__(self):
        self.configure()
        self.movie_ids = MovieFilter().load_feature_ids()
        self.features = {}
        self.feature_extractors = []
        for name, obj in inspect.getmembers(feature_extractors):
            if inspect.isclass(obj):
                self.feature_extractors.append(obj)

    def run(self):
        self.generate_feature_base()
        self.extract_features()
        self.save_features()

    def configure(self):
        arguments = docopt(__doc__, version='0.0.1')
        if arguments['--verbose']:
            logging.basicConfig(
                stream=sys.stdout,
                format=self.LOGGING_FORMAT,
            )
        else:
            logging.basicConfig(
                filename='feature_creator.log',
                format=self.LOGGING_FORMAT
            )
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def generate_feature_base(self):
        for movie, rating in self._load_movies_with_ratings():
            title = encode(movie.title)
            logging.info("Generating Base Features for %s (%s)" % (title, rating))
            self.features[int(movie.id)] = {
                'rating': float(rating),
                'rating_rounded': round(float(rating)),
                'title': title,
                'features': {}
            }

    def extract_features(self):
        for feature_extractor in self.feature_extractors:
            for movie_id, features in feature_extractor(self.movie_ids).extract_cached().iteritems():
                self.features[int(movie_id)]['features'].update(features)

    def save_features(self):
        Cache.save_file(self.FEATURES_PATH, self.features)

    def _load_movies_with_ratings(self):
        return session.query(
            models.Movie, models.MovieInfoIDX.info
        ).join(
            models.MovieInfoIDX
        ).filter(
            models.MovieInfoIDX.info_type_id==RATING_ID,
            models.Movie.id.in_(self.movie_ids)
        )


if __name__ == '__main__':
    FeatureCreator().run()