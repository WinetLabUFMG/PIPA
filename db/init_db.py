import psycopg2
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path("../backend/.env")
load_dotenv(dotenv_path)


conn = psycopg2.connect(
        host= os.getenv('DATABASE_URL'),
        port = os.getenv('DATABASE_PORT'),
        database= os.getenv('DB'),
        user= os.getenv('DB_USERNAME'),
        password= os.getenv('DB_PASSWORD'))

cur = conn.cursor()


cur.execute('DROP TABLE IF EXISTS usuarios;')

cur.execute('CREATE TABLE usuarios (username varchar (100) PRIMARY KEY NOT NULL,'
                                 'policyID integer[],'
                                 'firstName varchar (250) NOT NULL,'
                                 'lastName varchar (250) NOT NULL,'
                                 'fullName varchar (250) NOT NULL,'
                                 'email varchar (250) NOT NULL,'
                                 'isCreatedIPA BOOLEAN NOT NULL,'
                                 'isCreatedGitlab BOOLEAN NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

cur.execute('DROP TABLE IF EXISTS politicas;')

cur.execute('CREATE TABLE politicas (policyID serial PRIMARY KEY NOT NULL,'
                                 'name varchar (250) NOT NULL,'
                                 'projectsGitlab JSONB,'
                                 'groupIPA varchar(250),'
                                 'members varchar (250)[],'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

conn.commit()
cur.close()
conn.close()
