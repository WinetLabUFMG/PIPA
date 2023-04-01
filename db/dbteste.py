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


cur.execute('INSERT INTO usuarios (username, firstName, lastName, fullName, email, iscreatedipa, iscreatedgitlab)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    ('user01', 'USER', '01', 'USER01', 'user01@teste.com', False, False)
                    )

cur.execute('INSERT INTO usuarios (username, firstName, lastName, fullName, email, iscreatedipa, iscreatedgitlab)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    ('user02', 'USER', '02', 'USER02', 'user02@teste.com', False, False)
                    )

cur.execute('INSERT INTO usuarios (username, firstName, lastName, fullName, email, iscreatedipa, iscreatedgitlab)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    ('user03', 'USER', '03', 'USER03', 'user03@teste.com', False, False)
                    )


cur.execute('INSERT INTO usuarios (username, firstName, lastName, fullName, email, iscreatedipa, iscreatedgitlab)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    ('user04', 'USER', '04', 'USER04', 'user04@teste.com', False, False)
                    )

cur.execute('INSERT INTO usuarios (username, firstName, lastName, fullName, email, iscreatedipa, iscreatedgitlab)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    ('user05', 'USER', '05', 'USER05', 'user05@teste.com', False, False)
                    )
cur.execute('INSERT INTO usuarios (username, firstName, lastName, fullName, email, iscreatedipa, iscreatedgitlab)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    ('user06', 'USER', '06', 'USER06', 'user06@teste.com', False, False)
                    )
cur.execute('INSERT INTO usuarios (username, firstName, lastName, fullName, email, iscreatedipa, iscreatedgitlab)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    ('user07', 'USER', '07', 'USER07', 'user07@teste.com', False, False)
                    )

cur.execute('INSERT INTO usuarios (username, firstName, lastName, fullName, email, iscreatedipa, iscreatedgitlab)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    ('user08', 'USER', '08', 'USER08', 'user08@teste.com', False, False)
                    )


cur.execute('INSERT INTO politicas (name, projectsgitlab, groupipa)'
                    'VALUES (%s, %s, %s)',
                    ('Grupo A01', '{"lins": {"id": 6, "name": "lins"}, "pipa": {"id": 4, "name": "pipa"}, "aduna": {"id": 7, "name": "aduna"}, "lemonade": {"id": 5, "name": "lemonade"}}', 'ufmg_2021_a01')
                    )


cur.execute('INSERT INTO politicas (name, projectsgitlab, groupipa)'
                    'VALUES (%s, %s, %s)',
                    ('Grupo A02', '{"lins": {"id": 6, "name": "lins"}, "pipa": {"id": 4, "name": "pipa"}}', 'ufmg_2021_a02')
                    )

cur.execute('INSERT INTO politicas (name, projectsgitlab, groupipa)'
                    'VALUES (%s, %s, %s)',
                    ('Grupo C01', '{"lemonade": {"id": 5, "name": "lemonade"}}', 'ufmg_2021_c01')
                    )


conn.commit()
cur.close()
conn.close()