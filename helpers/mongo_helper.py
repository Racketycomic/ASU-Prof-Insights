from dotenv import load_env
import os

load_env()


ASU_DB=os.getenv('ASU_DB')
PROF_TABLE = os.getenv('PROF_TABLE')

def insert_profs(client,document):
    client[ASU_DB][PROF_TABLE].insert(document)