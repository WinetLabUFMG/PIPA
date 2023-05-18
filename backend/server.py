from flask import Flask, redirect, session, request, make_response, render_template, jsonify
from flask_cors import CORS
from flask_session import FileSystemSessionInterface
import json, requests, warnings, contextlib
from flask_restful import Api
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity,
                                create_access_token, create_refresh_token, 
                                set_access_cookies, set_refresh_cookies, 
                                unset_jwt_cookies,unset_access_cookies)

from urllib3.exceptions import InsecureRequestWarning
from authlib.integrations.flask_client import OAuth
from authlib.integrations.requests_client import OAuth2Session
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.oauth2.rfc7523 import ClientSecretJWT

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
OAUTH_CLIENT_KEY = os.getenv('OAUTH_CLIENT_KEY')
OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET')


# Services
from services.freeIPA  import FreeIPA
from services.gitLab import GitLab

IPA = FreeIPA(FREEIPA_DOMAIN, FREEIPA_ROOT_USERNAME, FREEIPA_ROOT_PASSWORD )
GL  = GitLab(GITLAB_DOMAIN, GITLAB_ROOT_USERNAME, GITLAB_ROOT_PASSWORD)

# autenticação com OAuth e WSO2
app = Flask("PAPA - Backend")
CORS(app)

old_merge_environment_settings = requests.Session.merge_environment_settings
app.config['BASE_URL'] = 'http://localhost:3000'  #Running on localhost
app.config['JWT_SECRET_KEY'] = '_dgUDB/DT4567"%8tgV*HYe'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_CSRF_CHECK_FORM'] = True
jwt = JWTManager(app) 

@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        # Verification happens only once per connection so we need to close
        # all the opened adapters once we're done. Otherwise, the effects of
        # verify=False persist beyond the end of this context manager.
        opened_adapters.add(self.get_adapter(url))

        settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
        settings['verify'] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_environment_settings

        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    # No auth header
    return redirect(app.config['BASE_URL'] + '/noauthheader', 302)

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    # Invalid Fresh/Non-Fresh Access token in auth header
    resp = make_response(redirect(app.config['BASE_URL'] + '/invalidfreshaccesstoken'))
    unset_jwt_cookies(resp)
    return resp, 302

@jwt.expired_token_loader
def expired_token_callback(callback):
    # Expired auth header
    resp = make_response(redirect(app.config['BASE_URL'] + '/token/refresh'))
    unset_access_cookies(resp)
    return resp, 302


oauth = OAuth()
oauth.init_app(app)

client_id = 'gVXPQX0P0ffBUn2gs9aG9LGGRtsa'
client_secret ='4aHj9_6vCenphTTWzZHvEhafp4ca'
token_endpoint = 'https://150.164.10.89:9443/oauth2/token'
redirect_uri=  'http://localhost:5000/callback'
scope = ['openid email']

client = OAuth2Session(client_id=client_id, client_secret=client_secret, scope=scope, redirect_uri=redirect_uri)

oauth.register(
    name='wso2',
    client_id= 'gVXPQX0P0ffBUn2gs9aG9LGGRtsa',
    client_secret= '4aHj9_6vCenphTTWzZHvEhafp4ca',
    access_token_endpoint= 'https://150.164.10.89:9443/oauth2/token',
    access_token_params=None,
    authorize_endpoint= 'https://150.164.10.89:9443/oauth2/authorize',
    authorize_params=None,
    api_base_url='https://150.164.10.89:9443/',
    client_kwargs={'scope': 'openid email'},
    redirect_uri=  'http://localhost:5000/callback',
    callback_url = 'https://localhost:3000/home',
    userinfo_endpoint= "https://150.164.10.89:9443/oauth2/userinfo",

)

@app.route("/")
def home():
    return "<h1>Hello Word</h1>"

@app.route("/login")
def login():
    authorization_uri = 'https://150.164.10.89:9443/oauth2/authorize'
    uri, state = client.create_authorization_url(authorization_uri)

    return uri

@app.route("/callback")
def callback():
    with no_ssl_verification():

        authorization_response = request.url
        token_endpoint = 'https://150.164.10.89:9443/oauth2/token'
        url = 'http://localhost:3000/home'

        token = client.fetch_token(token_endpoint, authorization_response=authorization_response)
        access_token = token['id_token']
        refresh_token = token['refresh_token']


        resp = make_response(redirect(url, 302))
        #resp.headers['Authorization'] = access_token
        print("para aqui", url)

        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)

        print(token)

        return resp
    
@app.route("/logout")
def unset_jwt():
    resp = make_response(redirect(app.config['BASE_URL'] + '/', 302))
    unset_jwt_cookies(resp)
    return resp

@app.route("/auth")
def auth():
    if "access_token_cookie" in request.cookies:
        return True
    else:
        return False, "Not authorized. Token invalid or not found"


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