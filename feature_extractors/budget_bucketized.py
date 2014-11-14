from feature_extractor_base import Base
from budget import BUDGET_RE
from helpers import encode
from models.info_type import BUDGET_TYPE_ID

import logging
import re

BUDGET_BUCKET = 5000000.0

class BudgetBucketizedFeatureExtractor(Base):
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
            except:
                logging.debug("Error parsing budget: %s" % budget)
                continue
            if features.get(movie_id) is None:
                features[movie_id] = {}
            existing_budget = features[movie_id].get('budget_bucket', 0)
            if existing_budget > 0:
                budget_int = max(budget_int, existing_budget)
            # bucketize budgets
            budget_bucket = int(round(budget_int / BUDGET_BUCKET))
            features[movie_id]['budget_bucket_%d' % budget_bucket] = 1
            logging.debug("Extracted budget: %s %s -> %d -> %d" % (movie_id, budget, budget_int, budget_bucket))
        return features
