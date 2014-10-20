from feature_extractor_base import Base
from helpers import encode
from models.info_type import VOTES_ID

import logging

class VotesFeatureExtractor(Base):
    oracle = True

    def get_votes(self):
        return self.session.query(
            self.models.MovieInfoIDX.movie_id,
            self.models.MovieInfoIDX.info
        ).filter(
            self.models.MovieInfoIDX.movie_id.in_(self.movie_ids),
            self.models.MovieInfoIDX.info_type_id == VOTES_ID
        ).distinct(
            self.models.MovieInfoIDX.movie_id
        )

    def extract(self):
        features = {}
        for movie_id, votes in self.get_votes():
            votes = int(votes)
            if features.get(movie_id) is None:
                features[movie_id] = {}
            features[movie_id]['votes'] = votes
            logging.debug("Extracted votes: %s %d" % (movie_id, votes))
        return features
