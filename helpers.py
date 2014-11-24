import logging
import math
from scipy import sparse
from sklearn import decomposition


MINIMUM_FEATURE_COUNT = 3


def encode(text):
    return text.decode('iso-8859-1').encode('utf8')

def normalize_features(data):
    logging.info("Normalizing features...")
    # First find max and min for each feature
    max_min = {}
    for movie_id, movie_info in data.items():
        for feature_name, feature_value in movie_info['features'].items():
            if feature_name in max_min:
                if max_min[feature_name][0] < feature_value:
                    max_min[feature_name][0] = feature_value
                if max_min[feature_name][1] > feature_value:
                    max_min[feature_name][1] = feature_value
            else:
                max_min[feature_name] = [feature_value, feature_value]

    # Normalize features
    for movie_id, movie_info in data.items():
        for feature_name, feature_value in movie_info['features'].items():
            if max_min[feature_name][0] == max_min[feature_name][1]:
                # max == min for this feature
                movie_info['features'][feature_name] = 1
            else:
                movie_info['features'][feature_name] = (feature_value - max_min[feature_name][1]) / float(max_min[feature_name][0] - max_min[feature_name][1])
    logging.info("Normalizing features done!")

def standard_eror(predictions, labels):
    if len(predictions) != len(labels):
        raise Exception("Number of predictions doesn't agree to number of labels")

    sum_squared_error = 0
    for i in range(len(predictions)):
        sum_squared_error += pow(predictions[i] - labels[i], 2)

    err = math.sqrt(sum_squared_error / len(predictions))

    logging.info("Standard error: %s" % err)
    return err

class DataTransformer(object):
    """
    DataTransformer transforms movie data we get from feature extractors to data we can use to pass into models in scikit-learn.
    Use:
        transformer = DataTransformer(data, training_movie_ids)
        feature_matrix, labels = transformer.get_training_data()
        scikit-learn.model.fit(feature_matrix, labels)

        data_of_movies_to_predict = (some data)
        scikit-learn.model.predict(transformer.transform_movies_data(data, predict_movie_ids))
    """
    def __init__(self, data, training_movie_ids, rounded_rating=False, run_pca=True, sparse_matrix=True):
        logging.info("Initializing DataTransformer...")
        self.rounded_rating = rounded_rating
        self.run_pca = run_pca
        self.sparse_matrix = sparse_matrix

        # Maps feature name to it's index in feature vector
        feature_name_to_count = {}
        for movie_id in training_movie_ids:
            if str(movie_id) not in data:
                continue
            movie_data = data[str(movie_id)]
            for feature_name in movie_data['features']:
                if feature_name not in feature_name_to_count:
                    feature_name_to_count[feature_name] = 1
                else:
                    feature_name_to_count[feature_name] += 1

        # Drop features
        self.feature_name_to_index = {}
        logging.info("Number of features before drop: %s" % len(feature_name_to_count))
        drop_feature_threshold = 0.001
        for feature_name, feature_count in feature_name_to_count.items():
            if feature_count >= MINIMUM_FEATURE_COUNT:
                self.feature_name_to_index[feature_name] = len(self.feature_name_to_index)
        logging.info("Number of features after drop: %s" % len(self.feature_name_to_index))

        # num_movies * num_features matrix.
        self.feature_matrix = []
        # num_movies array.
        self.labels = []
        for movie_id in training_movie_ids:
            if str(movie_id) not in data:
                continue
            movie_data = data[str(movie_id)]
            self.feature_matrix.append(self.transform_features(movie_data['features']))
            if self.rounded_rating:
                self.labels.append(movie_data['rating_rounded'])
            else:
                self.labels.append(movie_data['rating'])

        if self.sparse_matrix:
            self.feature_matrix = sparse.csr_matrix(self.feature_matrix)
        if self.run_pca:
            logging.info("Fitting pca...")
            self.pca = decomposition.RandomizedPCA(copy=False, n_components=7000)
            self.feature_matrix = self.pca.fit_transform(self.feature_matrix)
            logging.info("PCA fit")

        logging.info("Initializing DataTransformer done!")

    def get_training_data(self):
        return self.feature_matrix, self.labels

    def transform_features(self, feature_dict):
        '''
        Returns a sparse array with lenth = len(self.feature_name_to_index)
        '''
        feature_array = [0] * len(self.feature_name_to_index)
        for feature_name, feature_value in feature_dict.iteritems():
            if feature_name in self.feature_name_to_index:
                feature_array[self.feature_name_to_index[feature_name]] = feature_value
        return feature_array

    def transform_movies_data(self, data, predict_movie_ids):
        logging.info("Transforming movie data...")
        matrix = []
        labels = []
        ids = []  # In case predict_movie_id cannot be found in data
        for movie_id in predict_movie_ids:
            if str(movie_id) not in data:
                continue
            movie_data = data[str(movie_id)]
            matrix.append(self.transform_features(movie_data['features']))
            if self.rounded_rating:
                labels.append(movie_data['rating_rounded'])
            else:
                labels.append(movie_data['rating'])
            ids.append(movie_id)

        if self.sparse_matrix:
            matrix = sparse.csr_matrix(matrix)
        if self.run_pca:
            matrix = self.pca.transform(matrix)
        logging.info("Transforming movie data done!")
        return matrix, labels, ids

