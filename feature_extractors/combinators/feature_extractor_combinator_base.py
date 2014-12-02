from cache import Cache

# Combinators generate combinations of features per movie.
class Base():
    # Override this when you're developing
    __cache__ = True

    def extract_cached(self):
        cache_file = os.path.join('data', 'cache', 'combinators', '%s.json' % (self.__class__.__name__))
        return Cache.cache(self.__cache__, cache_file, self.extract)

    def combine(self, movie_id, features):
        raise NotImplementedError
