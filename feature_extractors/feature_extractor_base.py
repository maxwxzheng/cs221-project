import os

from cache import Cache
from session import session
import models


class Base(object):
    # Override this when you're developing
    __cache__ = True

    # Override if it shouldn't be in the oracle, or should be in the baseline.
    oracle = False
    baseline = True

    def __init__(self, movie_ids):
        self.session = session
        self.models = models
        self.movie_ids = movie_ids

    def extract_cached(self):
        cache_file = os.path.join('data', 'cache', '%s.json' % (self.__class__.__name__))
        return Cache.cache(self.__cache__, cache_file, self.extract)

    # This is the only required method
    # It should return a hash with keys that are movie ids, and values that
    # are hashes of features
    def extract(self):
        raise NotImplementedError

    def segmented_movie_ids(self, segment_size=500):
        """Yield movie ids in chunks"""
        tmp_movie_ids = []
        for movie_id in self.movie_ids:
            tmp_movie_ids.append(movie_id)
            if len(tmp_movie_ids) == segment_size:
                yield tmp_movie_ids
                tmp_movie_ids = []
        if len(tmp_movie_ids) > 0:
            yield tmp_movie_ids

    def movies_query(self):
        return self.session.query(
            self.models.Movie
        ).filter(
            self.models.Movie.id.in_(self.movie_ids)
        )