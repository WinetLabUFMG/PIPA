from flask import Flask 
from flask_cors import CORS
from flask import request
import json



import sys
sys.path.insert(0,"..")
from db import userDB
from db import politicaDB

# Environment variables 
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path("./.env")
load_dotenv(dotenv_path)

FREEIPA_DOMAIN = os.getenv('FREEIPA_DOMAIN')
FREEIPA_ROOT_USERNAME = os.getenv('FREEIPA_ROOT_USERNAME')
FREEIPA_ROOT_PASSWORD = os.getenv('FREEIPA_ROOT_PASSWORD')
GITLAB_DOMAIN = os.getenv('GITLAB_DOMAIN')
GITLAB_ROOT_USERNAME = os.getenv('GITLAB_ROOT_USERNAME')
GITLAB_ROOT_PASSWORD = os.getenv('GITLAB_ROOT_PASSWORD')


# Services
from services.freeIPA  import FreeIPA
from services.gitLab import GitLab

IPA = FreeIPA(FREEIPA_DOMAIN, FREEIPA_ROOT_USERNAME, FREEIPA_ROOT_PASSWORD )
GL  = GitLab(GITLAB_DOMAIN, GITLAB_ROOT_USERNAME, GITLAB_ROOT_PASSWORD)


app = Flask("PAPA - Backend")
CORS(app)


@app.route("/")
def home():
    return "<h1>Hello Word</h1>"


@app.route("/user", methods= ['GET', 'POST', 'PUT', 'DELETE'])
def user():
        
    if request.method == 'GET':
        username = request.args.get("username")
        
        if username == None:
            users = userDB.getAllUsers()
            return users
        else:
            user = userDB.getUser(username)
            return json.dumps(user)

    if request.method == 'POST':

        data = request.get_json()

        firstName = (data['firstName']).capitalize()
        lastName  = (data['lastName']).capitalize()
        fullName = firstName + " " + lastName
        email = data['email']
        userName = data['username']

        result = userDB.insertUser(userName, firstName, lastName, fullName, email)

        return result

    if request.method == 'PUT':
        
        data = request.get_json()

        firstName = (data['firstName']).capitalize()
        lastName  = (data['lastName']).capitalize()
        fullName = firstName + " " + lastName
        email = data['email']
        userName = data['username']
        userUpdate = data['userupdate']

        result = userDB.updateUser(userUpdate, userName, firstName, lastName, fullName, email)

        return result

    if request.method == 'DELETE':
        data = request.get_json()

        userToDelete = data['usertodelete']

        result = userDB.deleteUser(userToDelete)

        return result


@app.route("/user/create", methods = ['POST'])
def createUser():

    try:
        data = request.get_json()
        userName = data['username']
    
        result = userDB.getUser(userName)
        
        userName = result['username']
        firstName = result['firstname']
        lastName  = result['lastname']
        
        #email = result[5]
        
        # The full name is the same as the username because LDAP uses full name as cn
        fullName = result['username']
    
        # Add user in FreeIPA
        userIPA = IPA.addUserIPA(firstName, lastName, fullName, userName)
        randonPassword = userIPA['result']['randompassword']
        print("A senha e: ", randonPassword)
    
        # Authenticate to GitLab to create a user
        GL.createUserGitLab(userName, randonPassword)
        
        # TO DO
        # UPDATE USER IN DB
        userDB.updateServicesFlags(userName)
        
        return "Sucesso ao criar o usuário: " + userName

    except Exception as erro:
        return "Failed to create user: " + str(erro)



@app.route("/user/policy", methods = ['POST'])
def userPolicy():

    try:
        data = request.get_json()
        userNames = data['usernames']
        policyID = data['policyid']
    
        for user in userNames:
            userDB.updatePolicyID(user, policyID)

        politicaDB.updatePolicyMembers(policyID, userNames)

        return "Sucesso ao atribuir uma política para o(s) usuário(s)" 

    except Exception as erro:
        return "Failed to update policy id of user: " + str(erro)

    
@app.route("/gitlab")
@app.route("/gitlab/project", methods = ['GET', 'POST'])
def projectGitLab():
    

    if request.method == 'GET':
        return GL.getProjectsGitLab()

    if request.method == 'POST':

        data = request.get_json()

        usernames  = data['usernames']
        projects = data['projects']
        accessLevel= 'Developer'

        
        for user in usernames:
            for project in projects:
                projectID = projects[project]['id']
                GL.putUserInAProject(user, projectID, accessLevel)

        return 'Sucesso ao associar os usuários aos projetos do GitLab'


@app.route("/ipa")
@app.route("/ipa/getGroups", methods = ['GET'])
def getGroupsIPA():
    return IPA.getGroupsIPA()

@app.route("/ipa/group", methods = ['POST'])
def groupIPA():

    try:
        if request.method == 'POST':

            data = request.get_json()

            usernames  = data['usernames']
            groupIPA = data['grupoIPA']

            print(data)
           
            for user in usernames:
                IPA.putUserInGroupIPA(user, groupIPA)
            
            return 'Sucesso ao associar os usuários no grupo do FreeIPA'
        
    except Exception as error:
             return "Failed to put users in a FreeIPA group" + str(error)



@app.route("/policy", methods = ['GET', 'POST', 'PUT', 'DELETE'])
def policiesPIPA():

    if request.method == 'GET': 
        policyID = request.args.get("policyid")

        if policyID == None:
            try:
                policies = politicaDB.getAllPolicies()
                return policies
            except Exception as error:
                return "Failed to get the policy from database: " + str(error)
        else:
            try:
                policy = politicaDB.getPolicy(policyID)
                return json.dumps(policy)
            except Exception as error:
                return "Failed to get the policy from database: " + str(error)

    if request.method == 'POST':

        try:
            data = request.get_json()
            
            policyName = data['policyname']
                 
            projectsGitLab = {}
            for p in data['projectsgitlab']:
                pID = p['value']
                pName = p['label']
                pGL = {pName: {"id": pID, "name": pName}}
                projectsGitLab.update(pGL)
                
            groupIPA = data['groupipa']['name']

            result = politicaDB.insertPolicy(policyName, projectsGitLab, groupIPA)
            
            return result

        except Exception as error:
             return "Failed to insert the policy into database:" + str(error)

    if request.method == 'PUT':
        try:
            data = request.get_json()

            policyID   = data['policyid'] 
            policyName = data['policyname']
            projectsGitLab  = data['projectsgitlab']
            groupIPA = data['groupipa']

            result = politicaDB.updatePolicy(policyID, policyName, projectsGitLab, groupIPA)

            return result

        except Exception as error:
            return "Failed to update policy data in database: " + str(error)

    if request.method == 'DELETE':
        try:
            data = request.get_json()

            policyToDelete = data['policytodelete']
            result = politicaDB.deletePolicy(policyToDelete)

            return result

        except Exception as error:
            return "Failed to delete the policy in database: " + str(error)



@app.route("/policy/members", methods = ['GET', 'POST'])
def policyMembers():


    if request.method == 'GET': 
        policyID = request.args.get("policyid")
        
        try:
            result = politicaDB.getMemberPolicy(policyID)
            return result
        
        except Exception as error:
            return "Failed to get the members of a policy from the database: " + str(error)
       

app.run(debug=True)