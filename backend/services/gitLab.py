import gitlab
import os
import requests
from selenium import webdriver

class GitLab():

    def __init__ (self, GITLAB_DOMAIN, GITLAB_ROOT_USERNAME, GITLAB_ROOT_PASSWORD):
        self.GITLAB_DOMAIN = GITLAB_DOMAIN
        self.GITLAB_ROOT_USERNAME = GITLAB_ROOT_USERNAME
        self.GITLAB_ROOT_PASSWORD = GITLAB_ROOT_PASSWORD

    def createUserGitLab(self, userName, randonPassword):
        driver = webdriver.Chrome()
        driver.get(self.GITLAB_DOMAIN+'/users/sign_in')

        id_box = driver.find_element("name", 'username')
        id_box.send_keys(userName)

        pass_box = driver.find_element("name", 'password')
        pass_box.send_keys(randonPassword)


        login_button = driver.find_element("name", 'commit')
        login_button.submit()
    

    def createConnectionWithGitLab(self):
        res = requests.post(self.GITLAB_DOMAIN+'/oauth/token',
                        data={
                            "grant_type" : "password",
                            "username"   : self.GITLAB_ROOT_USERNAME,
                            "password"   : self.GITLAB_ROOT_PASSWORD
                        })
        
        token = res.json()
        token = token['access_token']

        gl = gitlab.Gitlab(url=self.GITLAB_DOMAIN, oauth_token=token, api_version=4) 

        return gl

    def getProjectsGitLab(self):

        try:
            gl = self.createConnectionWithGitLab()

            projects = gl.projects.list()
            dictOfProjects = {}

            for p in projects:
                dictOfProjects.update( {p.name:{'value': p.id, 'label': p.name }})

            return dictOfProjects
        
        except Exception as erro:
             return "Failed to get projecst in Gitlab: " + str(erro)


    def userIsMemberOfAProject(self, userName, idProject):
        try:
            gl = self.createConnectionWithGitLab()

            project = gl.projects.get(idProject)
            members = project.members.list()

            membersList = []

            for user in members:
                membersList.append(user.username)

            if(userName in membersList):
                print(userName)
                return True
            else:
                return False
        
        except Exception as erro:
             return "Failed to verify user: " + str(erro)


    def putUserInAProject(self, userName, idProject, accessLevel):

        try:

            if(self.userIsMemberOfAProject(userName, idProject)):
                print("O usuário " + userName + " já é membro do projeto!")
                return "O usuário " + userName + " já é membro do projeto!"
            else:
                gl = self.createConnectionWithGitLab()

                user = gl.users.list(search=userName)
                idUser = user[0].id

                project = gl.projects.get(idProject)

                if(accessLevel == 'Guest'):
                    accessLevel = gitlab.const.AccessLevel.GUEST
                if(accessLevel == 'Reporter'):
                    accessLevel = gitlab.const.AccessLevel.REPORTER
                if(accessLevel == 'Developer'):
                    accessLevel = gitlab.const.AccessLevel.DEVELOPER
                if(accessLevel == 'Maintainer'):
                    accessLevel = gitlab.const.AccessLevel.MAINTAINER
                if(accessLevel == 'Owner'):
                    accessLevel = gitlab.const.AccessLevel.OWNER

                member = project.members.create({ 'user_id': idUser,
                                                'access_level': accessLevel})

                return "O usuário " + userName + " foi adicionado ao projeto com sucesso!"

        except Exception as erro:
            return "Failed to put user in a Gitlab project: " + str(erro)



    # Need to finalize
    def putUserInGroupGitLab(self, userName):
 
        gl = self.createConnectionWithGitLab()

        user = gl.users.list(search=userName)
        idUser = user[0].id

        groups = gl.groups.list()
        group = groups[2]

        members = group.members.list()
        member = group.members.create({'user_id': idUser,
                                        'access_level': gitlab.const.AccessLevel.DEVELOPER})
