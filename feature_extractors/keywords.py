from feature_extractor_base import Base
from helpers import encode


class KeywordFeatureExtractor(Base):
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
        for keyword, movie_id in self.get_movie_keywords():
            keyword = encode(keyword)
            if features.get(movie_id) is None:
                features[movie_id] = {}
            features[movie_id][keyword] = 1
        return features