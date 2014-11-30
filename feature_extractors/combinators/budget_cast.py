import logging

from feature_extractor_combinator_base import Base

class BudgetCastCombinator(Base):
    def combine(self, movie_id, features):
        budget = 0
        cast = []
        for k, v in features.iteritems():
            if k.find('budget_bucket_') == 0:
                budget = k
            if k.find('cast_') == 0:
                cast.append(k)
        if budget != 0:
            for c in cast:
                features['%s_%s' % (budget, c)] = 1
