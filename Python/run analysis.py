import pandas as pd
import numpy as np
import string 
import psycopg2
import matplotlib as mpl
from sqlalchemy import create_engine

## pull data from db
db_str = 'postgres://127.0.0.1:5432/tt'
df = pd.read_sql('select t.dttm,h.hashtag from hashtags h inner join tweets t on t.id = h.tweet_id',create_engine(db_str))
