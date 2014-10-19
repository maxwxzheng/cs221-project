import math
import os
import random

from sqlalchemy import distinct

from cache import Cache
from session import session
from models.info_type import RATING_ID, GROSS_ID, VOTES_ID, RELEASE_DATES_ID
import models


class MovieFilter(object):
    TEST_PROB = 0.2
    DEV_IDS_PATH = os.path.join('data', 'dev.json')
    TEST_IDS_PATH = os.path.join('data', 'test.json')

    HAS_RATING = (
        models.MovieInfoIDX,
        (models.MovieInfoIDX.info_type_id==RATING_ID,)
    )

    HAS_US_RELEASE = (
        models.MovieInfo,
        (models.MovieInfo.info_type_id==RELEASE_DATES_ID, models.MovieInfo.info.like('USA:%'))
    )

    HAS_1000_VOTES = (
        models.MovieInfoIDX,
        (models.MovieInfoIDX.info_type_id==VOTES_ID, models.MovieInfoIDX.info > 1000)
    )

    HAS_US_GROSS = (
        models.MovieInfo,
        (models.MovieInfo.info_type_id==GROSS_ID, models.MovieInfo.info.like('%$%'))
    )

    CONDITIONS = (HAS_RATING, HAS_US_RELEASE, HAS_1000_VOTES, HAS_US_GROSS)

    def __init__(self):
        pass

    def load_feature_ids(self):
        if os.path.exists(self.DEV_IDS_PATH) and os.path.exists(self.TEST_IDS_PATH):
            movie_ids = (
                Cache.load_file(self.DEV_IDS_PATH) +
                Cache.load_file(self.TEST_IDS_PATH)
            )
        else:
            movie_ids = [id[0] for id in self.fetch_distinct_ids()]
            test_sample_size = int(math.floor(self.TEST_PROB * len(movie_ids)))
            test_ids = random.sample(movie_ids, test_sample_size)
            dev_ids = list(set(movie_ids) - set(test_ids))

            Cache.save_file(self.DEV_IDS_PATH, dev_ids)
            Cache.save_file(self.TEST_IDS_PATH, test_ids)

        print "Loaded %s Movie IDs" % (len(movie_ids))

        return movie_ids

    def fetch_distinct_ids(self):
        query = session.query(distinct(models.Movie.id))
        query = self._add_conditions(query)
        return query.all()

    def _add_conditions(self, query):
        for model, conditions in self.CONDITIONS:
            query = query.join(model, aliased=True).filter(*conditions)
        return query