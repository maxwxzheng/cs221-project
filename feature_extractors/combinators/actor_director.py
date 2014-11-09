import logging
import re

from feature_extractor_combinator_base import Base

CAST_RE = "cast_([\d]+)_([\d]+)"

class ActorDirectorCombinator(Base):
    def combine(self, movie_id, features):
        actors = []
        directors = []
        for k, v in features.iteritems():
            if k.find('cast_') == 0:
                match = re.match(CAST_RE, k)
                if not match or match.lastindex != 2:
                    continue
                person_id = match.group(1)
                role = match.group(2)
                if role == '8':
                    directors.append(person_id)
                if role == '1' or role == '2':
                    actors.append(person_id)
        pairs = [(a, d)for a in actors for d in directors]
        logging.debug('Combining %s: %s' % (movie_id, pairs))
        for p in pairs:
            features['c_%s_%s' % (p[0], p[1])] = 1
