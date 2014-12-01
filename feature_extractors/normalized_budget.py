import logging

from feature_extractor_base import Base
from models.info_type import BUDGET_TYPE_ID, RELEASE_DATES_ID
from sqlalchemy import types
from sqlalchemy.orm.util import aliased
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import cast

"""
Extracts max budget (USD) and min release year per movie.
Averages budgets per year, and outputs a single new feature per movie:
    normalized_budget = budget - average(budget that year)
"""

class NormalizedBudgetFeatureExtractor(Base):

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
        average_budgets = {}
        counts = {}
        data = list(self.get_data())
        for movie_id, budget, release_year in data:
            average_budgets[release_year] = average_budgets.get(release_year, 0) + budget
            counts[release_year] = counts.get(release_year, 0) + 1
        for year, sum in average_budgets.iteritems():
            average_budgets[year] = int(sum / counts[year])
        logging.info('budget averages: ',  average_budgets)
        print average_budgets

        features = {}
        for movie_id, budget, release_year in data:
            if features.get(movie_id) is None:
                features[movie_id] = {}
            normalized_budget = int(budget) - average_budgets[release_year]
            features[movie_id]['normalized_budget'] = normalized_budget
            logging.debug(
                'Extracted normalized budget: %s %s %s -> %s' %
                (movie_id, str(budget), str(average_budgets[release_year]),
                str(normalized_budget))
            )
        return features
