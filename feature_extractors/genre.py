from feature_extractor_base import Base
from helpers import encode


class GenreFeatureExtractor(Base):
    def get_genre(self):
        return self.session.query(
            self.models.MovieInfo.movie_id,
            self.models.MovieInfo.info
        ).filter(
            self.models.MovieInfo.movie_id.in_(self.movie_ids),
            self.models.MovieInfo.info_type_id.in_([3]), # 3 is the info_type_id for 'genre'
        ).distinct(
            self.models.CastInfo.movie_id
        )

    def extract(self):
        features = {}
        for movie_id, genre in self.get_genre():
            genre = encode(genre)
            if self.__debug__:
                print "Extracted Genre: ", movie_id, genre
            if features.get(movie_id) is None:
                features[movie_id] = {}
            features[movie_id]['genere_%s' % (genre)] = 1
        return features