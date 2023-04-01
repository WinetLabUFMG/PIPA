from python_freeipa import ClientMeta



class FreeIPA:

    def __init__ (self, FREEIPA_DOMAIN, FREEIPA_ROOT_USERNAME, FREEIPA_ROOT_PASSWORD):
        self.FREEIPA_DOMAIN = FREEIPA_DOMAIN
        self.FREEIPA_ROOT_USERNAME = FREEIPA_ROOT_USERNAME
        self.FREEIPA_ROOT_PASSWORD = FREEIPA_ROOT_PASSWORD


    def ipaAuth(self):

        client = ClientMeta(self.FREEIPA_DOMAIN, verify_ssl=False)
        client.login(self.FREEIPA_ROOT_USERNAME, self.FREEIPA_ROOT_PASSWORD)

        return client
        
  
    def addUserIPA(self, firstName, lastName, fullName, userName):
        

        try:
            client = self.ipaAuth()
            user = client.user_add(a_uid= userName, 
                                o_givenname=firstName, 
                                o_sn=lastName, 
                                o_cn=fullName,
                                o_random=True,
                                o_preferredlanguage='EN'
                                )

            return user
            
        except (Exception) as erro:
            return "Failed to add user in FreeIPA " + str(erro)

    def getGroupsIPA(self):
        
        try:
            client = self.ipaAuth()
            groups = client.group_find()

            dictOfGroupsIPA = {}

            for g in groups['result']:
                if 'gidnumber' in g:
                    dictOfGroupsIPA.update( {g['cn'][0]:{'id': g['gidnumber'][0], 'name': g['cn'][0] }})
            
            return dictOfGroupsIPA

        except (Exception) as erro:
            return "Failed to get groups in FreeIPA " + str(erro)
        


    def putUserInGroupIPA(self, userName, groupName):

        try:
            client = self.ipaAuth()

            #group = client.group_find(o_gidnumber= groupID)
            #group_cn = group['result'][0]['cn'][0]
            group_cn = groupName

            client.group_add_member(a_cn=group_cn, o_user=userName)

        except (Exception) as erro:
            return "Failed to put user in a group in FreeIPA " + str(erro)




        


       
