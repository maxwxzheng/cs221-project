CS221 Project
=============

Adding a feature extractor
--------------------------

Add a new file in the feature_extractors folder containing a class inhering
from Base, implementing the extract method:


    from feature_extractor_base import Base


    class SomeFeatureExtractor(Base):
        __cache__ = False

        def extract(self):
            return {'MOVIE_ID_1': {'my_crazy_feature': 1}}


Registration is automatic, just import your feature extractor in
`feature_extractors/__init__.py`.

    from keywords import SomeFeatureExtractor

You'll probably want to set `__cache__ = False` while you're developing.  When
`__cache__ = True`, the results of extract will be stored in a json file in
the `data/cache` folder, which will prevent feature extractors that you
aren't working on from running.

The feature extractor will have the instance variables `self.session`,
`self.models`, and `self.movie_ids` set.

- `self.session`: A SQLAlchemy session; used for querying the db.
- `self.models`: SQLAlchemy models for each table in the db.
- `self.movie_ids`: An array of all of the movie ids we're using.

In addition, the feature extractor base class provides a few helper
functions:

- `segmented_movie_ids`: this will yield movie_ids in chunks of 500 by default,
  making it a little easier to split up queries.
- `movies_query`: this is just a base query to get all the movies we care about,
  you can string addional stuff onto this.
- `with_appearances`: this can be used to get the number of times a feature
  appears in the dataset, and eliminate features that don't appear enough.

Checkout the `KeywordFeatureExtractor` for a decent example of what the logic
should look like.

By default, FeatureExtractors are included in the baseline, and not exclusive
to the oracle.  To add a feature to the oracle, set `oracle = True` in the
feature extractors class.

Setup
-----

You'll want to install all the packages in requirements.txt.  In addition,
you should copy config.yaml.example to config.yaml, and change anything
you need to for your mysql server.


Running This
------------

Just run the feature_creator.py file.

    python feature_creator.py

ID's for dev and test set will be in data folder, as will features.json.


Logging
-------

Use the python logging module.

    import logging
    logging.debug("Some log message")

By default, it will log in feature_creator.log.  Set `--verbose` to print
logging messages to stdout.


SQLAlchemy
----------

Pretty solid docs starting at http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html.


Weirdness
---------

The mysql char encoding has some issues, so text should be re-encoded before
it's used.  There's a helper method called `encode` in `helper.py` that can
do this.  Please use this method, so we can get rid of this
(or at least work around it consistently).

Caveat: I wrote this quickly and there aren't tests.  There are probably bugs.
Some stuff could definitely be cleaned up, like session handling and imports.