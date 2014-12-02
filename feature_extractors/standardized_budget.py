import logging
import numpy

from feature_extractor_base import Base
from models.info_type import BUDGET_TYPE_ID, RELEASE_DATES_ID
from sqlalchemy import types
from sqlalchemy.orm.util import aliased
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import cast

"""
Extracts max budget (USD) and min release year per movie.
Computes data for combinators/compute_standardized_budget.py
"""

class StandardizedBudgetFeatureExtractor(Base):

    def get_data(self):
        logging.debug("These queries will take a few mins to run.")

        budget_query = self.session.query(
            self.models.MovieInfo.movie_id,
            func.max(
                cast(
                    func.replace(
                        func.replace(self.models.MovieInfo.info, ",", ""),
                        "$", ""),
                    types.Numeric)
            ).label('budget')
        ).filter(
            self.models.MovieInfo.movie_id.in_(self.movie_ids),
            self.models.MovieInfo.info_type_id.in_([BUDGET_TYPE_ID]),
            self.models.MovieInfo.info.like('$%'),
        ).group_by(self.models.MovieInfo.movie_id
        ).subquery()

        year_query = self.session.query(
            self.models.MovieInfo.movie_id,
            func.min(
                func.substr(self.models.MovieInfo.info, -4)
            ).label('release_year')
        ).filter(
            self.models.MovieInfo.movie_id.in_(self.movie_ids),
            self.models.MovieInfo.info_type_id.in_([RELEASE_DATES_ID]),
            self.models.MovieInfo.info.like('USA:%')
        ).group_by(self.models.MovieInfo.movie_id
        ).subquery()

        budget_alias = aliased(self.models.MovieInfo, budget_query)
        year_alias = aliased(self.models.MovieInfo, year_query)

        return self.session.query(
            budget_query.columns.movie_id,
            budget_query.columns.budget,
            year_query.columns.release_year
        ).join(
            year_alias, year_alias.movie_id == budget_alias.movie_id
        ).distinct(
            self.models.MovieInfo.movie_id
        ).filter(
            self.models.MovieInfo.movie_id.in_(self.movie_ids),
        )

    def extract(self):
        budgets = {}
        data = list(self.get_data())
        for movie_id, budget, release_year in data:
            if budgets.get(release_year) is None:
                budgets[release_year] = []
            budgets[release_year].append(int(budget)),

        features = {}
        for movie_id, budget, release_year in data:
            if features.get(movie_id) is None:
                features[movie_id] = {}
            features[movie_id]['standardized_budget'] = {
                'budget': int(budget),
                'year_data': budgets[release_year],
            }
            logging.debug(
                'Extracted standardized budget: %s (%s, %s)' %
                (movie_id, str(budget), str(release_year))
            )
        return features
