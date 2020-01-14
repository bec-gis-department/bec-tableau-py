from bec_tableau.bec_tsm import *
import itertools

#Call the Method sending it hardplastic Encryption
tsm_method = bec_tsm_data_methods('encrypteduser', 'encryptedpwd')

#Generate the Authorization Token
tableau_auth = tsm_method.tableau_auth()

#Use that Token to connect to the Server URL
server = tsm_method.server_sign_in(tableau_auth, 'url-to-server')

projects = tsm_method.list_workbooks(server)

for x, y in zip(projects[0], projects[1]):
    if x == 'Workbook Name you are looking for':
        print x