import logging
import numpy

from feature_extractor_combinator_base import Base

class ComputeStandardizedBudget(Base):
    def combine(self, movie_id, features):
        budget_data = features.get('standardized_budget')
        if budget_data == None:
            return

        mean = numpy.mean(budget_data['year_data'])
        std = numpy.std(budget_data['year_data'])

        if std != 0:
            standardized_budget = (budget_data['budget'] - mean) / std
        else:
            standardized_budget = 0
        features['standardized_budget'] = standardized_budget
        logging.debug(
            'Computed standardized budget: %s (%s - %s) / %s = %s' %
            (movie_id, str(budget_data['budget']), str(mean), str(std),
            str(standardized_budget))
        )
