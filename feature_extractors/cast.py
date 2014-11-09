import logging

from feature_extractor_base import Base
from helpers import encode


class CastFeatureExtractor(Base):
    MINIMUM_APPEARANCES = 2

    def get_cast(self):
        logging.debug("These queries will take a few mins to run.")

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
        )

    def extract(self):
        features = {}
        # appearances is how many movies the person has appeared in
        for movie_id, person_id, role_id, role, name, appearances in self.with_appearances(
            self.get_cast(),
            self.MINIMUM_APPEARANCES,
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
            features[movie_id]['cast_%s_%s' % (person_id, role_id)] = 1
        return features