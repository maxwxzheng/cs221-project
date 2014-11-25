"""
PCA Analyzer

Usage:
  pca_analyzer.py [options]

Options:
  -h --help             Show this screen.
  --feature-file=FILE   Json file containing features [default: data/features.json]
"""

from docopt import docopt
from sklearn import decomposition
import json
import contextlib
import os
import helpers
from cache import Cache
import itertools
import logging
import sys
import time
import csv


class PCAAnalyzer(object):

    def run(self):
        self.arguments = docopt(__doc__)
        self.load_data()
        self.perform_pca()

    def load_data(self):
        logging.info("Starting data loading")
        self.data = json.load(open(self.arguments['--feature-file']))
        helpers.normalize_features(self.data)

        self.dev_movie_ids = json.load(open('data/dev.json'))
        self.test_movie_ids = json.load(open('data/test.json'))

        # Transforms the data so they can be used by scikit-learn library.
        self.data_transformer = helpers.DataTransformer(self.data, self.dev_movie_ids, run_pca=False)
        self.training_feature_matrix, self.training_labels = self.data_transformer.get_training_data()

        self.predict_feature_matrix, self.predict_labels, self.predict_ids = \
            self.data_transformer.transform_movies_data(self.data, self.test_movie_ids)
        logging.info("Data loading complete")

    def perform_pca(self):
        for components in [5000]:
            pca = decomposition.TruncatedSVD(n_components=components)
            logging.info("Fitting pca for %s components..." % components)
            start = time.time()
            pca.fit(self.training_feature_matrix)
            logging.info("PCA fit - %s explained" % pca.explained_variance_ratio_.sum())
            logging.info("Fitting time - %s" % str(time.time() - start))

            with open(os.path.join('data', 'pca.csv'), 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Feature Number', 'Variance Ratio', 'Cumulative Variance'])
                for i in range(components):
                    writer.writerow([
                        i+1,
                        pca.explained_variance_ratio_[i],
                        pca.explained_variance_ratio_[0:i+1].sum()
                    ])


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    PCAAnalyzer().run()