import psycopg2
from psycopg2.extras import Json, RealDictCursor
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path("../backend/.env")
load_dotenv(dotenv_path)


def startConnectionDB():

    try:
        conn = psycopg2.connect(
                host= os.getenv('DATABASE_URL'),
                port = os.getenv('DATABASE_PORT'),
                database= os.getenv('DB'),
                user= os.getenv('DB_USERNAME'),
                password= os.getenv('DB_PASSWORD'))

        cur = conn.cursor(cursor_factory=RealDictCursor)

        return cur, conn
    
    except(Exception, psycopg2.Error) as error:
       return "Failed to connect to the database" + str(error)



def closeConnectionDB(cur, conn):
    cur.close()
    conn.close()



def insertUser(username, firstName, lastName, fullName , email):
    
    try:
        cur, conn = startConnectionDB()

        cur.execute('INSERT INTO usuarios (username, firstName, lastName, fullName, email, iscreatedipa, iscreatedgitlab)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (username, firstName, lastName, fullName, email, False, False)
                    )
        
        conn.commit()

        closeConnectionDB(cur, conn)

        return "Sucesso ao adicionar o usuário " + username
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to insert user into database:" + str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)




def getUser(username):
    try:
        cur, conn = startConnectionDB()

        cur.execute("SELECT username, policyid, firstname, lastname, fullname, email, iscreatedipa, iscreatedgitlab FROM usuarios WHERE username = %s", (username,))
        
        result = cur.fetchone()
        
        closeConnectionDB(cur, conn)
        return result

        
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to get user from database: " + str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)



def updateUser(userUpdate, userName, firstName, lastName, fullName, email):
    try:
        cur, conn = startConnectionDB()

        cur.execute('''
                        UPDATE usuarios
                        SET 
                            username= %s,
                            firstName=%s,
                            lastName=%s,
                            fullName=%s,
                            email=%s
                        WHERE 
                            username=%s
                    '''
                    ,(userName, firstName, lastName, fullName, email, userUpdate)
                    )

        conn.commit()

        closeConnectionDB(cur, conn)

        return "Sucesso ao atulizar o usuário " + userName
        
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to update user data in database: " +  str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)


def deleteUser(usertodelete):
    try:
        cur, conn = startConnectionDB()

        cur.execute('DELETE FROM usuarios WHERE username=%s', (usertodelete,))

        conn.commit()

        closeConnectionDB(cur, conn)
        
        return "Sucesso ao deletar o usuário " + usertodelete
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to delete user in database: " + str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)



def updateServicesFlags(username):
    try:
        cur, conn = startConnectionDB()

        cur.execute('''
                        UPDATE usuarios
                        SET 
                            iscreatedipa= %s,
                            iscreatedgitlab=%s
                        WHERE 
                            username=%s
                    '''
                    ,(True, True, username)
                    )

        conn.commit()

        closeConnectionDB(cur, conn)

        return "Sucesso ao atualizar flags de serviço"
        
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to update services in database: " + str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)


def getAllUsers():
    try:
        cur, conn = startConnectionDB()

        cur.execute("SELECT username, policyid, firstname, lastname, fullname, email from usuarios")
        
        result = cur.fetchall()
        
        closeConnectionDB(cur, conn)
        return result

    
    except(Exception, psycopg2.Error) as error:
        return "Failed to get user from database:" + str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)



def updatePolicyID(username, policyID):
    try:
        cur, conn = startConnectionDB()
        cur.execute("SELECT policyid from usuarios where username=%s", (username,))
        result = cur.fetchone()

        policyIds = []

        policyIds.append(int(policyID))

        if(result['policyid'] != None):   
            for policies in result['policyid']:
                policyIds.append(int(policies))   

        print(policyIds)
        print(username)
 
       
        cur.execute(
                        '''
                        UPDATE usuarios
                        SET 
                            policyid= %s
                        WHERE 
                            username=%s
                        '''
                    ,(policyIds, username)
                    )

        conn.commit()
        closeConnectionDB(cur, conn)
        
        return "Sucesso ao atribuir uma política para o usuário"
        
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to update policy id of user: " + str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)
