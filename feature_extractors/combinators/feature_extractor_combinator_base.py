
# Combinators generate combinations of features per movie.
class Base():
    def combine(self, movie_id, features):
        raise NotImplementedError
