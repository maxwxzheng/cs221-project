import os
import json

class Cache(object):
    @classmethod
    def cache(cls, cache_enabled, filename, function):
        if cache_enabled:
            if os.path.isfile(filename):
                return cls.load_file(filename)
            else:
                data_to_cache = function()
                cls.save_file(filename, data_to_cache)
                return data_to_cache
        else:
            return function()

    @classmethod
    def load_file(cls, filename):
        with open(filename) as f:
            return json.loads(f.read())

    @classmethod
    def save_file(cls, filename, contents):
        with open(filename, 'w') as f:
            f.write(json.dumps(contents, indent=4, encoding="utf-8"))
