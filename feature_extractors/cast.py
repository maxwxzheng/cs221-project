from feature_extractor_base import Base
from helpers import encode


class CastFeatureExtractor(Base):
    def get_cast(self):
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
        for movie_id, person_id, role_id, role, name in self.get_cast():
            name = encode(name)
            role = encode(role)
            if self.__debug__:
                print "Extracted Actor: ", movie_id, person_id, role_id, role, name
            if features.get(movie_id) is None:
                features[movie_id] = {}
            features[movie_id]['cast_%s_%s' % (person_id, role_id)] = 1
        return features