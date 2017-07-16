from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import os
import sys

if 'PGPASSWORD' not in os.environ:
    sys.exit('ERROR: PGPASSWORD environment variable missing')

user = 'postgres'
password = os.environ['PGPASSWORD']

engine = create_engine(
    "postgresql+psycopg2://{}:{}@localhost/test".format(user, password))
Session = scoped_session(sessionmaker(bind=engine))
s = Session()
result = s.execute('SELECT * FROM test')
for row in result:
    print(row)
s.close()
