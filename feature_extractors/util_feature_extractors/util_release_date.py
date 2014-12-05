from models.info_type import RELEASE_DATES_ID

import logging
import re
import calendar

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from feature_extractor_base import Base

"""
Info format:
USA:August 2012
USA:31 August 2012

Features saved:
Store month and year of the first release.
"""

INFO_PREFIX = 'USA:'
RELEASE_DATE_DMY_RE = 'USA:\d+ (\w+) (\w+)'
RELEASE_DATE_MY_RE = 'USA:(\w+) (\w+)'

class UtilReleaseDateFeatureExtractor(Base):
    def get_releases(self):
        return self.session.query(
            self.models.MovieInfo.movie_id,
            self.models.MovieInfo.info,
        ).filter(
            self.models.MovieInfo.movie_id.in_(self.movie_ids),
            self.models.MovieInfo.info_type_id.in_([RELEASE_DATES_ID]),
            self.models.MovieInfo.info.like(INFO_PREFIX + '%')
        )

    def extract(self):
        month_name_to_number = dict((v,k) for k,v in enumerate(calendar.month_name))

        features = {}
        for movie_id, release in self.get_releases():
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
            year = int(match.group(2))

            if month in month_name_to_number:
                month_number = int(month_name_to_number[month])
            else:
                logging.debug("Movie (%s) release month is not recognized: %s" % (movie_id, month))

            update_release = False
            if "release_year" not in movie_feature:
                update_release = True
            elif movie_feature["release_year"] > year:
                update_release = True
            elif movie_feature["release_year"] == year and movie_feature["release_month"] > month_number:
                update_release = True

            if update_release:
                movie_feature["release_year"] = year
                movie_feature["release_month"] = month_number

                logging.debug('Extracted util release date (%s): %s %s' % (movie_id, month, year))
        return features
