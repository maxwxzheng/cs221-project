from feature_extractor_base import Base
from helpers import encode
from models.info_type import BUDGET_TYPE_ID

import logging
import re

BUDGET_RE = "\$([\d,]+)"

class BudgetFeatureExtractor(Base):
    def get_budget(self):
        return self.session.query(
            self.models.MovieInfo.movie_id,
            self.models.MovieInfo.info
        ).filter(
            self.models.MovieInfo.movie_id.in_(self.movie_ids),
            self.models.MovieInfo.info_type_id.in_([BUDGET_TYPE_ID]),
            self.models.MovieInfo.info.like('$%'),
        )

    def extract(self):
        features = {}
        for movie_id, budget in self.get_budget():
            match = re.match(BUDGET_RE, budget)
            if not match or match.lastindex != 1:
                logging.debug("Skipping budget: %s" % budget)
                continue

            budget_int = 0
            try:
                budget_int = int(match.group(1).replace(",", ""))
                logging.debug("Extracted budget: %s %s -> %d" % (movie_id, budget, budget_int))
            except:
                logging.debug("Error parsing budget: %s" % budget)
                continue
            if features.get(movie_id) is None:
                features[movie_id] = {}
            features[movie_id]['budget'] = max(features[movie_id].get('budget', 0), budget_int)
        return features
