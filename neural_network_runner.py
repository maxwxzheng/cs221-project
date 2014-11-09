import json
import os
import helpers
from cache import Cache
import itertools
import logging
import sys
import time

from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork


class NeuralNetworkRunner(object):
    def run(self):
        self.load_data()

        self.run_pybrain()

    def load_data(self):
        logging.info("Starting data loads.")
        self.data = json.load(open('data/features.json'))
        helpers.normalize_features(self.data)

        self.dev_movie_ids = set(json.load(open('data/dev.json')))
        self.test_movie_ids = set(json.load(open('data/test.json')))

        self.data = dict((k,self.data[unicode(k)]) for k in (list(self.dev_movie_ids)[0:900] + list(self.test_movie_ids)[0:100]))

        # Transforms the data so they can be used by pybrain.
        logging.info("Loading feature keys...")
        feature_keys = set()
        for movie_id, features in self.data.iteritems():
            feature_keys.update(features['features'].keys())

        self.feature_keys = list(feature_keys)
        logging.info("Feature keys loaded.")

        logging.info("Vectorizing features...")
        self.dev_features = []
        self.dev_scores = []
        self.test_features = []
        self.test_scores = []
        for movie_id, features in self.data.iteritems():
            if int(movie_id) in self.dev_movie_ids:
                features_list = self.dev_features
                scores_list = self.dev_scores
            else:
                features_list = self.test_features
                scores_list = self.test_scores

            features_list.append([features['features'].get(feature_key, 0) for feature_key in self.feature_keys])
            scores_list.append([features['rating']])
        logging.info("Features vectorized.")

    def run_pybrain(self):
        logging.info("Loading data")
        dev_set = SupervisedDataSet(len(self.feature_keys), 1)
        for features, score in itertools.izip(self.dev_features, self.dev_scores):
            dev_set.addSample(features, score)
        logging.info("Training data loaded")

        net = buildNetwork(len(self.feature_keys), 100, 100, 1, bias=True)
        trainer = BackpropTrainer(net, dev_set)
        print trainer.trainUntilConvergence(maxEpochs=100, verbose=True)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    NeuralNetworkRunner().run()