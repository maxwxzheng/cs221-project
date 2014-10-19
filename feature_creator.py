# -*- coding: utf-8 -*-
import inspect

from cache import Cache
from session import session
from movie_filter import MovieFilter
import models
import feature_extractors
from models.info_type import RATING_ID
import os
from helpers import encode


class FeatureCreator(object):
    FEATURES_PATH = os.path.join('data', 'features.json')

    def __init__(self):
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

    def generate_feature_base(self):
        for movie, rating in self._load_movies_with_ratings():
            title = encode(movie.title)
            print "Generating Base Features for %s (%s)" % (title, rating)
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


FeatureCreator().run()