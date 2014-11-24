"""
Fann Data Generator

Usage:
  fann_data_generator.py [options]

Options:
  -h --help             Show this screen.
  --feature-file=FILE   Json file containing features [default: data/features.json]
"""

from docopt import docopt
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
        self.arguments = docopt(__doc__)
        self.load_data()
        self.save_fann_files()

    def load_data(self):
        logging.info("Starting data loading")
        self.data = json.load(open(self.arguments['--feature-file']))
        helpers.normalize_features(self.data)

        self.dev_movie_ids = json.load(open('data/dev.json'))
        self.test_movie_ids = json.load(open('data/test.json'))

        # Transforms the data so they can be used by scikit-learn library.
        self.data_transformer = helpers.DataTransformer(self.data, self.dev_movie_ids)  # , run_pca=False, sparse_matrix=False)
        self.training_feature_matrix, self.training_labels = self.data_transformer.get_training_data()

        self.predict_feature_matrix, self.predict_labels, self.predict_ids = \
            self.data_transformer.transform_movies_data(self.data, self.test_movie_ids)
        logging.info("Data loading complete")

    def save_fann_files(self):
        files = (
            (os.path.join("data", "minimal.data"), self.training_feature_matrix[0:100], self.training_labels[0:100]),
            (os.path.join("data", "dev.data"), self.training_feature_matrix, self.training_labels),
            (os.path.join("data", "test.data"), self.predict_feature_matrix, self.predict_labels)
        )
        for file_name, matrix, labels in files:
            logging.info("Writing file %s" % file_name)
            with open(file_name, 'w') as file:
                file.write("%s %s %s\n" % (len(matrix), len(matrix[0]), 1))
                for row, rating in itertools.izip(matrix, labels):
                    feature_str = ' '.join(str(i) for i in row)
                    self.write_features_and_rating(file, feature_str, rating)

    def write_features_and_rating(self, file, feature_str, rating):
        file.write(feature_str)
        file.write("\n")
        # Convert to a 0 - 1.0 value
        file.write(str(rating / 10.0))
        file.write("\n")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    FannDataGenerator().run()