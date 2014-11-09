import logging

from feature_extractor_base import Base
from helpers import encode


class KeywordFeatureExtractor(Base):
    # only use common keywords that appears at least this many times
    KEYWORD_COUNT = 10

    def get_movie_keywords(self):
        for movie_ids in self.segmented_movie_ids():
            for result in self.session.query(
                self.models.Keyword.keyword, self.models.MovieKeyword.movie_id
            ).join(
                self.models.MovieKeyword
            ).filter(
                self.models.MovieKeyword.movie_id.in_(movie_ids)
            ):
                yield result

    def extract(self):
        features = {}
        # appearances is how many movies the keyword has been applied to
        for keyword, movie_id, appearances in self.with_appearances(
            self.get_movie_keywords(),
            self.KEYWORD_COUNT,
            lambda x: x[0],  # count of: keyword
            lambda x: x[1]   # that appears in: movie_id
        ):
            keyword = encode(keyword)
            logging.debug(
                "Extracted Keyword: %s %s %s" % (keyword, movie_id, appearances)
            )
            if features.get(movie_id) is None:
                features[movie_id] = {}
            features[movie_id][keyword] = 1
        return features