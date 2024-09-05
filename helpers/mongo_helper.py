from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv('../.env')


ASU_DB=os.getenv('ASU_DB')
PROF_TABLE = os.getenv('PROF_TABLE')
URI = os.getenv('MONGO_URI')



def get_connection():
    client = MongoClient(URI)
    return client

def insert_profs(client,document):
    client[ASU_DB][PROF_TABLE].insert_one(document)