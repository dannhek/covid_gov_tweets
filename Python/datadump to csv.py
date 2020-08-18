import pandas as pd 
from sqlalchemy import create_engine
from openpyxl import load_workbook

pg_eng = create_engine('postgresql://dhek:tr@127.0.0.1/tt')

tweets = pd.read_sql('tweets',pg_eng)
atusers = pd.read_sql('atusers',pg_eng)
hashtags = pd.read_sql('hashtags',pg_eng)
urlrefs = pd.read_sql('urlrefs',pg_eng)

excel = 'data model example.xlsx'
book = load_workbook(excel)
writer = pd.ExcelWriter(excel, engine = 'openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)    
tweets.to_excel(writer,sheet_name = 'tweets', index=False)
atusers.to_excel(writer,sheet_name = 'atusers', index=False)
hashtags.to_excel(writer,sheet_name = 'hashtags', index=False)
urlrefs.to_excel(writer,sheet_name = 'urlrefs', index=False)

writer.save()
writer.close()