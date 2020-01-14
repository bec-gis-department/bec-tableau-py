#-------------------------------------------------------------------------------
# Name:       XXXX Packaging
# Purpose:      Package Published Workbooks on a XXXX Schedule
#
# Author:      John Lister - GIS Applications Developer
#
# Created:     23/04/2019
# Copyright:   (c) BEC 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from bec_tableau.bec_tsm import *

import os

#Testing Commands
# Calls Methods to evaluate performance
#Local Environment Variables:
tableau_dir = r"Dev Path to Tableau Drive"

tableauProd_dir = r"Prod Path to Tableau Drive"

#Dev Outputs
newSvcOpenOrder_dir = os.path.join(tableau_dir,r"MemSvc\New Service Team\Open Orders")
energySvcScore_dir = os.path.join(tableau_dir,r"Sysops\Energy Services\Scorecard")

#Prod Outputs
pipConstruction_dir = os.path.join(tableauProd_dir, r"PIP\New-New")

#Dev Dest Locations
outTWBXdir = {
                'Dashboard 1': sysOps_SvcOrders_dir,
                'Dashboard 2': energySvcScore_dir
                }

#Prod Dest Locations
prod_outTWBXdir = {
    'Prod Dashboard 1': pipConstruction_dir
}


#Call the Method sending it hardplastic Encryption
## Use bec_decode to generate a somewhat encrypted password or store them in config file... your call
tsm_method = bec_tsm_data_methods('encrypted user', 'encrypted pwd')

#Generate the Authorization Token
tableau_auth = tsm_method.tableau_auth()


#----------------------------TABLEAU DEV----------------------------------------
#Here we want to fetch workbooks from the Tableau Server and Package them as TWBX
#Use that Token to connect to the Server URL

devServer = tsm_method.server_sign_in(tableau_auth, 'URL to Dev Server')
for key in outTWBXdir:
    print(key, outTWBXdir[key])
    tsm_method.package_workbook(devServer, [key], outTWBXdir[key])

#Make sure to sign out from the server when you are done
tsm_method.server_sign_out(devServer)

#-------------------------------------------------------------------------------
#-----------------------------TABLEAU PROD--------------------------------------
#Use that Token to connect to the Server URL
prodServer = tsm_method.server_sign_in(tableau_auth, 'URL to Prod Server')
#Here we want to fetch workbooks from the Tableau Server and Package them as TWBX
for key in prod_outTWBXdir:
    print(key, prod_outTWBXdir[key])
    tsm_method.package_workbook(prodServer, [key], prod_outTWBXdir[key])

#Make sure to sign out from the server when you are done
tsm_method.server_sign_out(prodServer)


del tsm_method