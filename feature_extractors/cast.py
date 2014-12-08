import csv
import logging
from collections import defaultdict

import numpy
from feature_extractor_base import Base
from helpers import encode
from models.info_type import RATING_ID
from models.role import ACTOR, ACTRESS, DIRECTOR, PRODUCER


class CastFeatureExtractor(Base):
    MINIMUM_APPEARANCES = 2

    def get_cast(self):
        logging.debug("Getting cast from MySQL... this will take a few mins to run.")

        return self.session.query(
            self.models.CastInfo.movie_id,
            self.models.CastInfo.person_id,
            self.models.CastInfo.role_id,
            self.models.Role.role,
            self.models.Person.name
        ).join(
            self.models.Person,
            self.models.Role
        ).filter(
            self.models.CastInfo.movie_id.in_(self.movie_ids)
        ).distinct(
            self.models.CastInfo.movie_id,
            self.models.CastInfo.person_id,
            self.models.CastInfo.role_id,
        ).all()

        logging.debug("Finished getting cast from MySQL")

    def load_movie_ratings_map(self):
        logging.debug("Loading movie ratings")

        query = self.session.query(
            self.models.Movie, self.models.MovieInfoIDX.info
        ).join(
            self.models.MovieInfoIDX
        ).filter(
            self.models.MovieInfoIDX.info_type_id==RATING_ID,
            self.models.Movie.id.in_(self.movie_ids)
        )
        movie_ratings = {}
        for movie, rating in query:
            movie_ratings[movie.id] = rating

        logging.debug("Movie ratings loaded")
        return movie_ratings

    def extract(self):
        features = {}
        appearances_per_movie = defaultdict(lambda: defaultdict(list))
        average_rating_per_movie = defaultdict(lambda: defaultdict(list))
        cast = self.get_cast()
        movie_ratings_map = self.load_movie_ratings_map()

        person_movie_rating_map = defaultdict(dict)
        for movie_id, person_id, role_id, role, name in cast:
            person_movie_rating_map[person_id][movie_id] = movie_ratings_map[movie_id]

        # appearances is how many movies the person has appeared in
        for movie_id, person_id, role_id, role, name, appearances in self.with_appearances(
            cast,
            0,  # Ignore minimum appearances
            lambda x: x[1],  # count of: person_id
            lambda x: x[0]   # that appears in: movie_id
        ):
            name = encode(name)
            role = encode(role)
            logging.debug(
                 "Extracted Actor: %s %s %s %s %s %s" %
                 (movie_id, person_id, role_id, role, name, appearances)
            )
            if features.get(movie_id) is None:
                features[movie_id] = {}
            if appearances >= self.MINIMUM_APPEARANCES:
                features[movie_id]['cast_%s_%s' % (person_id, role_id)] = 1

            appearances_per_movie[role_id][movie_id].append(appearances)

            person_ratings = [
                float(rating) for rated_movie_id, rating in person_movie_rating_map[person_id].iteritems()
                if not rated_movie_id == movie_id
            ]
            if person_ratings:
                average_rating_per_movie[role_id][movie_id].append(numpy.mean(person_ratings))

        self._add_bucket_features('appearances', features, appearances_per_movie)
        self._add_bucket_features('crew_ratings', features, average_rating_per_movie)

        return features

    def _calculate_features_from_numeric_list(self, numeric_list):
        features = {}
        if not numeric_list:
            return features
        features['mean'] = int(round(numpy.mean(numeric_list)))
        percentiles = [1, 10, 25, 50, 75, 90, 99]
        for percentile, value in zip(percentiles, numpy.percentile(numeric_list, percentiles)):
            features['%s_pctl' % percentile] = int(round(value))
        return features

    def _add_bucket_features(self, name, features, appearances_per_movie):
        numeric_features = ['mean'] + ['%s_pctl' % percentile for percentile in [1, 10, 25, 50, 75, 90, 99]]
        for roles in [[ACTOR], [ACTRESS], [ACTOR, ACTRESS], [DIRECTOR], [PRODUCER], range(1, 13)]:
            with open('data/%s-%s.csv' % (name, '-'.join([str(role) for role in roles])), 'w') as csvfile:
                writer = csv.writer(csvfile)

                writer.writerow(['Movie'] + numeric_features)
                for movie_id, appearances in self._merge_appearances(appearances_per_movie, roles).iteritems():
                    appearance_features = self._calculate_features_from_numeric_list(appearances)
                    row = [movie_id]
                    for numeric_feature in numeric_features:
                        bucket = appearance_features[numeric_feature]
                        if bucket > 20:
                            bucket = 20

                        row.append(bucket)
                        features[movie_id]['%s_%s_%s_%s' % (name, '-'.join([str(role) for role in roles]), numeric_feature, bucket)] = 1

                    writer.writerow(row)

    def _merge_appearances(self, appearances_per_movie, roles):
        merged_lists = defaultdict(list)
        for role in roles:
            for movie_id, appearances in appearances_per_movie[role].iteritems():
                merged_lists[movie_id].extend(appearances)
        return merged_lists