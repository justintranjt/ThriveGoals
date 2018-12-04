#!/usr/bin/env python

#-----------------------------------------------------------------------
# selectDB.py
# Author: Josh Gardner
#-----------------------------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import select
import os
import psycopg2


db_uri = "postgres://wrlppbbvqcauzp:764db7ff9a698abcadb0ecf37e5d3f6405fb5acf6a1f1802f2febad6f6e52dfe@ec2-50-16-196-138.compute-1.amazonaws.com:5432/d7p8464rd276rt"
#conn = psycopg2.connect(db_uri, sslmode='require')

#os.environ['DATABASE_URL']
engine = create_engine(db_uri)
conn = engine.connect()

metadata = MetaData(engine, reflect=True)
#print(metadata.tables)

# Get Table
template_table = metadata.tables['templates']


# select * from 'user'
select_st = select([template_table])
res = conn.execute(select_st)
for _row in res:
    print (_row[0])
    print (_row[1])
    print (_row[2])
    print("       ")
    print("       ")