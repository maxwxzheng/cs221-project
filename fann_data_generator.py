import json
import contextlib
import os
import helpers
from cache import Cache
import itertools
import logging
import sys
import time


class FannDataGenerator(object):
    MINIMAL_SIZE = 100

    def run(self):
        self.load_data()

    def load_data(self):
        logging.info("Starting data loads.")
        self.data = json.load(open('data/features.json'))

        self.dev_movie_ids = set(json.load(open('data/dev.json')))
        self.test_movie_ids = set(json.load(open('data/test.json')))

        # Transforms the data so they can be used by pybrain.
        logging.info("Loading feature keys...")
        feature_keys = set()
        for movie_id, features in self.data.iteritems():
            feature_keys.update(features['features'].keys())

        self.feature_keys = list(feature_keys)
        logging.info("Feature keys loaded.")

        logging.info("Vectorizing features...")
        i = 0
        with contextlib.nested(
            open(os.path.join("data", "minimal.data"), "w"),
            open(os.path.join("data", "test.data"), "w"),
            open(os.path.join("data", "dev.data"), "w")
        ) as (minimal_file, test_file, dev_file):
            minimal_file.write("%s %s %s\n" % (self.MINIMAL_SIZE, len(self.feature_keys), 1))
            test_file.write("%s %s %s\n" % (len(self.test_movie_ids), len(self.feature_keys), 1))
            dev_file.write("%s %s %s\n" % (len(self.dev_movie_ids), len(self.feature_keys), 1))

            for movie_id, features in self.data.iteritems():
                i += 1
                if int(movie_id) in self.dev_movie_ids:
                    file = dev_file
                else:
                    file = test_file

                full_feature = [str(features['features'].get(feature_key, 0)) for feature_key in self.feature_keys]
                full_feature_str = ' '.join(full_feature)

                if i <= self.MINIMAL_SIZE:
                    self.write_features_and_rating(minimal_file, full_feature_str, features['rating'])
                self.write_features_and_rating(file, full_feature_str, features['rating'])

        logging.info("Features vectorized.")

    def write_features_and_rating(self, file, feature_str, rating):
        file.write(feature_str)
        file.write("\n")
        file.write(str(rating))
        file.write("\n")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    FannDataGenerator().run()