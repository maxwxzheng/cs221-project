import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


config = yaml.load(open('config.yaml').read())
mysql_url = 'mysql://%s:%s@%s/%s' % (config['user'], config['password'], config['host'], config['db'])
print "Connecting to %s" % (mysql_url)
engine = create_engine(mysql_url, echo=True)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()