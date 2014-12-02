"""
Scikit Learn Runner

Usage:
  scikit_learn_runner.py [options]

Options:
  -h --help             Show this screen.
  --feature-file=FILE   Json file containing features [default: data/features.json]
"""

from docopt import docopt
import json
import os
import helpers
from sklearn import linear_model
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from cache import Cache
import logging
import sys
import time
import pickle

class ScikitLearnRunner(object):
    def run(self):
        self.arguments = docopt(__doc__)
        self.load_data()

        self.run_model(linear_model.LinearRegression(), "linear_regression")
        self.run_model(linear_model.LogisticRegression(C=0.8), "logistic_regressor")
        self.run_model(linear_model.SGDRegressor(shuffle=True, n_iter=100000), "sgd_regressor")

        #self.run_model(svm.SVR(), "svm")

    def load_data(self):
        self.data = json.load(open(self.arguments['--feature-file']))
        helpers.normalize_features(self.data)

        self.dev_movie_ids = json.load(open('data/dev.json'))
        self.test_movie_ids = json.load(open('data/test.json'))

        # Transforms the data so they can be used by scikit-learn library.
        self.data_transformer = helpers.DataTransformer(self.data, self.dev_movie_ids, run_pca=False)
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

        # Write result to file
        f = open('data/result/%s' % model_name, 'w')
        f.write(pickle.dumps(model))
        f.close()

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    ScikitLearnRunner().run()
