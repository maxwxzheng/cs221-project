import logging

from feature_extractor_combinator_base import Base

class BudgetCastCombinator(Base):
    def combine(self, movie_id, features):
        budget = 0
        cast = []
        for k, v in features.iteritems():
            if k == 'budget_bucket': budget = v
            if k.find('cast_') == 0:
                cast.append(k)
        if budget == 0:
            logging.debug('Skipping %s, no budget' % movie_id)
            return
        for c in cast:
            features['b_%d_%s' % (budget, c)] = 1
