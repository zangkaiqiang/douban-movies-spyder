import pymysql

from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://{username}:{password}@{hostname}/db?charset=utf8')
