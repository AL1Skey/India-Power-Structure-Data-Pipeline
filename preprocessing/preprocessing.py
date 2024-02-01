import os
import pandas as pd
from sqlalchemy import create_engine
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, BulkIndexError
from datetime import datetime

def feedsql():
    username = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    database = os.environ['POSTGRES_DB']
    host = os.environ['POSTGRES_HOST']
    
    pg_url = f'postgresql+psycopg2://{username}:{password}@{host}/{database}'
    engine = create_engine(pg_url)
    conn = engine.connect()
    
    cwd = os.getcwd()
    filelist = os.listdir(os.path.join(cwd,'dataset'))
    file = [i for i in filelist if '.csv' in i][0]
    
    df = pd.read_csv(f'/opt/airflow/dataset/{file}')
    df.to_sql('dirty',conn,index=False,if_exists='replace')
    
def feedcsv():
    username = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    database = os.environ['POSTGRES_DB']
    host = os.environ['POSTGRES_HOST']
    
    pg_url = f'postgresql+psycopg2://{username}:{password}@{host}/{database}'
    engine = create_engine(pg_url)
    conn = engine.connect()
    
    df = pd.read_sql_query('select * from dirty',conn)
    df.to_csv('/opt/airflow/dataset/dirty.csv',sep=',', index=False)

def preprocessing():
    df = pd.read_csv('/opt/airflow/dataset/dirty.csv')
    
    # Change Columns
    df.columns= ['teritory','year','power_spec','power_needed','kwh_needed','megawatt_capacity']
    
    # Missing Value Handling
    # - = SimpleImputter(0), . = SimpleImputter(0)
    df.replace('.','0',inplace=True)
    df.replace('-','0',inplace=True)
    
    # Change Data Type
    df[['power_spec','power_needed','megawatt_capacity']] = df[['power_spec','power_needed','megawatt_capacity']].astype(int)
    df['kwh_needed'] = df['kwh_needed'].astype(float)
    df['year'] = pd.to_datetime(df['year'])
    
    # Save Cleaned Data
    df.to_csv('/opt/airflow/dataset/clean.csv',index=False,sep=',')

def upload_to_elasticsearch():
    es = Elasticsearch("http://elasticsearch:9200")
    df = pd.read_csv('/opt/airflow/dataset/clean.csv')
    for i, r in df.iterrows():
        doc = r.to_dict()  # Convert the row to a dictionary
        res = es.index(index="india_powersupply", id=i+1, 
                       body=doc, 
                       #op_type="index"
                       )
        print(f"Response from Elasticsearch: {res}")

def upload_to_elasticsearch():
    es = Elasticsearch("http://elasticsearch:9200")
    df = pd.read_csv('/opt/airflow/dataset/clean.csv')
    # Persiapkan data untuk pengindeksan paket besar
    actions = [
        {"_op_type": "index", "_index": "india_powersupply", "_id": i+1, "_source": doc.to_dict()}
        for i, doc in df.iterrows()
    ]
    try:
        # Gunakan bulk indexing untuk mengirimkan data sekaligus
        success, failed = bulk(es, actions=actions, index="india_powersupply")
        print(f"Successfully indexed: {success}")
        if failed:
            print(f"Failed to index: {failed}")
    except BulkIndexError as e:
        print(f"Bulk indexing failed: {e}")
        # You can also access detailed information about the errors
        for error in e.errors:
            print(f"Error details: {error}")
        raise Exception()
    