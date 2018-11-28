#!/usr/bin/env python

#-----------------------------------------------------------------------
# createDB.py
# Author: Josh Gardner
#-----------------------------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String, Boolean, PickleType
import os
import psycopg2


db_uri = "postgres://wrlppbbvqcauzp:764db7ff9a698abcadb0ecf37e5d3f6405fb5acf6a1f1802f2febad6f6e52dfe@ec2-50-16-196-138.compute-1.amazonaws.com:5432/d7p8464rd276rt"
conn = psycopg2.connect(db_uri, sslmode='require')
#os.environ['DATABASE_URL']
engine = create_engine(db_uri)
#conn = engine.connect()
meta = MetaData(engine)


templates = Table('templates', meta,
	       Column('username', String),
           Column('templateName', String),
           Column('templateJSON', String)
           )


# users = Table('users', meta,
#            Column('username',String, primary_key=True),
#            Column('password',String)),

# Create all tables in meta
meta.create_all()