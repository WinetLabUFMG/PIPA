from apache_ranger.model.ranger_service import *
from apache_ranger.client.ranger_client import *
from apache_ranger.model.ranger_policy  import *
from apache_ranger.client.ranger_client          import *
from apache_ranger.model.ranger_policy           import *
from apache_ranger.model.ranger_service          import *
from apache_ranger.model.ranger_service_resource import *
from apache_ranger.model.ranger_service_tags     import *
from apache_ranger.model.ranger_tagdef           import *
from apache_ranger.model.ranger_tag              import *
from datetime                                    import datetime

class Ranger:
     
     def __init__ (self, RANGER_URL, RANGER_USERNAME, RANGER_PASSWORD):
        self.RANGER_URL = RANGER_URL
        self.RANGER_USERNAME = RANGER_USERNAME
        self.RANGER_PASSWORD = RANGER_PASSWORD

## Step 1: create a client to connect to Apache Ranger admin
ranger_url  = RANGER_URL
ranger_auth = (RANGER_USERNAME, RANGER_PASSWORD)

# For Kerberos authentication
#
# from requests_kerberos import HTTPKerberosAuth
#
# ranger_auth = HTTPKerberosAuth()

ranger = RangerClient(ranger_url, ranger_auth)

# to disable SSL certificate validation (not recommended for production use!)
ranger.session.verify = False

## atributos úteis de uma política

def putUserInPolicyRanger(self, )

policy             = RangerPolicy()
policy.service     = service_name
policy.name        = policy_name
policy.description = 'test description'
policy.resources   = { 'database': RangerPolicyResource({ 'values': ['test_db'] }),
                       'table':    RangerPolicyResource({ 'values': ['test_tbl'] }),
                       'column':   RangerPolicyResource({ 'values': ['*'] }) }
policy.add_resource({ 'database': RangerPolicyResource({ 'values': ['test_db1'] }),
                      'table':    RangerPolicyResource({ 'values': ['test_tbl1'] }),
                      'column':   RangerPolicyResource({ 'values': ['*'] }) })
policy.add_resource({ 'database': RangerPolicyResource({ 'values': ['test_db2'] }),
                      'table':    RangerPolicyResource({ 'values': ['test_tbl2'] }),
                      'column':   RangerPolicyResource({ 'values': ['*'] }) })



allowItem1          = RangerPolicyItem()
'''
{
  "users" : [ "...", "..." ],
  "accesses" : [ {
    "isAllowed" : true,
    "type" : "..."
  }, {
    "isAllowed" : true,
    "type" : "..."
  } ],
  "groups" : [ "...", "..." ],
  "roles" : [ "...", "..." ],
  "conditions" : [ {
    "values" : [ "...", "..." ],
    "type" : "..."
  }, {
    "values" : [ "...", "..." ],
    "type" : "..."
  } ],
  "delegateAdmin" : true
}
'''
allowItem1.users    = [ 'admin' ]
allowItem1.accesses = [ RangerPolicyItemAccess({ 'type': 'create' }),
                        RangerPolicyItemAccess({ 'type': 'alter' }),
                        RangerPolicyItemAccess({ 'type': 'select' }) ]

policy.policyItems     = [ allowItem1 ]

created_policy = ranger.create_policy(policy)

print('    created policy: id: ' + str(created_policy.id) + ', name: ' + created_policy.name)

policy_id = created_policy.id


created_policy = ranger.create_policy(policy)

print('Updating policy: id=' + str(policy_id))

saved_value                = created_policy.description
created_policy.description = 'updated description - #1'

updated_policy1 = ranger.update_policy_by_id(policy_id, created_policy)