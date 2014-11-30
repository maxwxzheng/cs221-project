"""
Scikit Kmeans Runner

Usage:
  scikit_kmeans_runner.py [options]

Options:
  -h --help             Show this screen.
  --clusters=CLUSTERS   Number of clusters - if this isn't specified multiple clusters are created.
"""

from docopt import docopt
import json
import os
import helpers
from sklearn import cluster
from cache import Cache
import itertools
import logging
import sys
import time
import pickle

class ScikitKmeansRunner(object):
    def run(self):
        self.arguments = docopt(__doc__)
        self.load_data()

        counts = [int(self.arguments['--clusters'])] if self.arguments['--clusters'] else [10, 100, 500, 1000]

        for count in counts:
            self.run_model(cluster.KMeans(n_clusters=count, verbose=5, n_jobs=-1, precompute_distances=True, copy_x=False), "k_means_%s" % count)

    def load_data(self):
        self.data = json.load(open('data/features.json'))
        helpers.normalize_features(self.data)

        self.dev_movie_ids = json.load(open('data/dev.json'))
        self.test_movie_ids = json.load(open('data/test.json'))

        # Transforms the data so they can be used by scikit-learn library.
        self.data_transformer = helpers.DataTransformer(self.data, self.dev_movie_ids, run_pca=False, sparse_matrix=True)
        self.training_feature_matrix, self.training_labels = self.data_transformer.get_training_data()

        self.predict_feature_matrix, self.predict_labels, self.predict_ids = \
            self.data_transformer.transform_movies_data(self.data, self.test_movie_ids)

    def run_model(self, model, model_name):
        logging.info("Fitting model %s..." % model_name)
        start = time.time()
        model.fit(self.training_feature_matrix, self.training_labels)
        logging.info("Fitting model %s done! Took %s seconds." % (model_name, time.time() - start))

        logging.info("Predicting using model %s..." % model_name)
        start = time.time()
        predictions = model.predict(self.predict_feature_matrix)
        logging.info("Predicting using model %s done! Took %s seconds." % (model_name, time.time() - start))

        helpers.standard_eror(predictions, self.predict_labels)

        self.save_kmeans_features(model, model_name)

        # The model when there are 1000 clusters is too large to save
        # Write result to file
        # f = open('data/result/%s' % model_name, 'w')
        # f.write(pickle.dumps(model))
        # f.close()

    def save_kmeans_features(self, model, model_name):
        logging.info("Preparing to save kmeans features...")
        logging.info("Reloading features.")
        features = json.load(open('data/features.json'))
        logging.info("Generating clusters for data")
        training_predictions = model.predict(self.training_feature_matrix)
        test_predictions = model.predict(self.predict_feature_matrix)
        logging.info("Finished Generating Clusters for data")

        movie_id_clusters = [[self.dev_movie_ids, training_predictions], [self.test_movie_ids, test_predictions]]

        for movie_ids, clusters in movie_id_clusters:
            if len(movie_ids) != len(clusters):
                raise ValueError('Movie ids don\'t match clusters')
            for movie_id, cluster in itertools.izip(movie_ids, clusters):
                features[str(movie_id)]['features']['cluster_%s' % cluster] = 1

        logging.info("Saving cluster features")

        Cache.save_file(os.path.join('data', 'features_%s.json' % model_name), features)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    ScikitKmeansRunner().run()
