from feature_extractor_base import Base
from helpers import encode
from models.info_type import RELEASE_DATES_ID

import logging
import re

"""
Info format:
USA:August 2012
USA:31 August 2012

Note format:
NULL
(Sundance Film Festival) (premiere)
(premiere)
(Telluride Film Festival)
(Dimension 3 Film Festival) (Premiere)
(New York City, New York) (NYC Horror Film Festival) (premiere) 

Features saved:
Store the date for the festival and location (if parsed)
Treat null entries as premieres
For each of the above, store month and year (both separately and combined).
"""

INFO_PREFIX = 'USA:'
RELEASE_DATE_DMY_RE = 'USA:\d+ (\w+) (\w+)'
RELEASE_DATE_MY_RE = 'USA:(\w+) (\w+)'

class ReleaseDateFeatureExtractor(Base):
    def get_releases(self):
        return self.session.query(
            self.models.MovieInfo.movie_id,
            self.models.MovieInfo.info,
            self.models.MovieInfo.note
        ).filter(
            self.models.MovieInfo.movie_id.in_(self.movie_ids),
            self.models.MovieInfo.info_type_id.in_([RELEASE_DATES_ID]),
            self.models.MovieInfo.info.like(INFO_PREFIX + '%')
        )

    def extract(self):
        features = {}
        for movie_id, release, note in self.get_releases():
            match = re.match(RELEASE_DATE_DMY_RE, release)
            if not match or match.lastindex != 2:
                match = re.match(RELEASE_DATE_MY_RE, release)
                if not match or match.lastindex != 2:
                    logging.debug("Error parsing (%s): %s" % (movie_id, release))
                    continue

            if features.get(movie_id) is None:
                features[movie_id] = {}
            movie_feature = features[movie_id]

            month = match.group(1)
            year = match.group(2)

            if note == None:
                # assume NULL means premiere
                note = 'premiere'
            note = note.lower()
            for part in note.split(') ('):
                part = part.replace('(', '')
                part = part.replace(')', '')
                part = encode(part)

                movie_feature['release (%s) (%s)' % (part, month)] = 1
                movie_feature['release (%s) (%s)' % (part, year)] = 1
                movie_feature['release (%s) (%s %s)' % (part, month, year)] = 1
                logging.debug('Extracted release date (%s): %s -> %s %s' %
                              (movie_id, part, month, year))
        return features
