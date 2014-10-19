from feature_extractor_base import Base
from helpers import encode
from models.info_type import GENRE_TYPE_ID

import logging

class GenreFeatureExtractor(Base):
    def get_genre(self):
        return self.session.query(
            self.models.MovieInfo.movie_id,
            self.models.MovieInfo.info
        ).filter(
            self.models.MovieInfo.movie_id.in_(self.movie_ids),
            self.models.MovieInfo.info_type_id.in_([GENRE_TYPE_ID]),
        ).distinct(
            self.models.MovieInfo.movie_id
        )

    def extract(self):
        features = {}
        for movie_id, genre in self.get_genre():
            genre = encode(genre)
            logging.debug("Extracted Genre: %s %s" % (movie_id, genre))
            if features.get(movie_id) is None:
                features[movie_id] = {}
            features[movie_id]['genere_%s' % (genre)] = 1
        return features