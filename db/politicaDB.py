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



def insertPolicy(policyName, projectsGitLab, groupipa):
    
    try:
        cur, conn = startConnectionDB()

        cur.execute('INSERT INTO politicas (name, projectsgitlab, groupipa)'
                    'VALUES (%s, %s, %s)',
                    (policyName, Json(projectsGitLab), groupipa)
                    )
        
        conn.commit()

        closeConnectionDB(cur, conn)

        return "Sucesso ao adicionar política!"
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to insert the policy into database:" + str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)




def getPolicy(policyID):
    try:
        cur, conn = startConnectionDB()

        cur.execute("SELECT policyid, name, projectsgitlab, groupipa, members FROM politicas WHERE policyID = %s", (policyID,))
        
        result = cur.fetchone()
        
        closeConnectionDB(cur, conn)
        return result
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to get the policy from database:" + str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)



def updatePolicy(policyID, policyName, projectsGitLab, groupipa):
    try:
        cur, conn = startConnectionDB()

        cur.execute('''
                        UPDATE politicas
                        SET 
                            name= %s,
                            projectsgitlab=%s,
                            groupipa=%s
                        WHERE 
                            policyID=%s
                    '''
                    ,(policyName, Json(projectsGitLab), groupipa, policyID)
                    )

        conn.commit()

        closeConnectionDB(cur, conn)

        return "Sucesso em atualizar política!"
        
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to update policy data in database: " +  str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)


def deletePolicy(policyID):
    try:
        cur, conn = startConnectionDB()

        cur.execute('DELETE FROM politicas WHERE policyID=%s', (policyID,))

        conn.commit()

        closeConnectionDB(cur, conn)
        
        return "Sucesso em deletar política!"
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to delete the policy in database: " + str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)



def getAllPolicies():
    try:
        cur, conn = startConnectionDB()

        cur.execute("SELECT * FROM politicas")
        
        result = cur.fetchall()
        
        closeConnectionDB(cur, conn)
        return result

    
    except(Exception, psycopg2.Error) as error:
        return "Failed to get policy from database:" + str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)


def updatePolicyMembers(policyID, members):
    try:
        cur, conn = startConnectionDB()

        cur.execute('''
                        UPDATE politicas
                        SET 
                            members=%s
                        WHERE 
                            policyID=%s
                    '''
                    ,(members, policyID)
                    )

        conn.commit()

        closeConnectionDB(cur, conn)

        return "Sucesso em inserir membros na política!"
        
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to insert members policy data into database: " +  str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)


def getMemberPolicy(policyID):
    try:
        cur, conn = startConnectionDB()

        cur.execute("SELECT members FROM politicas WHERE policyID = %s", (policyID,))
        
        result = cur.fetchone()
        
        closeConnectionDB(cur, conn)
        return result
    
    except(Exception, psycopg2.Error) as error:
        return "Failed to get the members of a policy from the database:" + str(error)
    
    finally:
        if conn:
            closeConnectionDB(cur, conn)
