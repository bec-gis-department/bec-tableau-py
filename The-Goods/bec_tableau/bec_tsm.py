#-------------------------------------------------------------------------------
# Name:        TSC Methods
# Purpose:     BEC Modulaized Tableau Server Cllient Methods
#
# Author(s):
#               J Lister - GIS Applications Developer
#               D Flisowski - IT Applications Analyst
# Created:     11/04/2019
# Copyright:   (c) uaserver 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#Custom Python Modules
from bec_decode.simplestic_plastic import *
from general_functions import *

#Tableau Server Client
import tableauserverclient as TSC

#Python Standard Libraries
import glob
import sys
import os

class bec_tsm_data_methods:
    def __init__(self, enc_usr, enc_pwd):
        self.user = enc_usr
        self.pwd = enc_pwd
        self.req_option = TSC.RequestOptions(pagesize=1000)

    def tableau_auth(self):
        """
            Created: 04/11/2019
            Description:
                Generate the tableau Authorization Object using the encrypted User & PWD
            Returns:
                Tableau Authorization Object
        """
        try:
            tableau_auth = TSC.TableauAuth(softplastic(self.user), softplastic(self.pwd))
        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])
            sys.exit()
        return tableau_auth

    def server_sign_in(self, tableau_auth, server_url):
        """
            Created: 04/11/2019
            Description:
                Establish connection to the Tableau server using the AUTH & Server
            Returns:
                Tableau Server Object
        """
        try:
            server = TSC.Server(server_url)
            server.use_server_version()
            server.auth.sign_in(tableau_auth)
            return server
        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])
            sys.exit()

    def server_sign_out(self, server):
        """
            Created: 04/11/2019
            Description:
                Kills connection to the Tableau server
            Returns:
                N/A
        """
        server.auth.sign_out()

    def fetch_datasources(self, server, server_datasource_names, out_dir):
        """
            Created: 04/11/2019
            Description:
                Download Datasource(s) defined in SERVER_DATASOURCE_NAMES from the SERVER

        """
        # Gets all datasource items
        all_datasources = list(TSC.Pager(server.datasources, self.req_option))
        ##all_datasources, pagination_item = server.datasources.get()
        for datasource in all_datasources:
            #Fetch the datasource ID's we need
            if datasource.name in server_datasource_names:
                print("Downloading {0} to {1}".format(str(datasource.id), out_dir))
                server.datasources.download(datasource.id, filepath=out_dir, no_extract=False)

    def list_projects(self, server):
        """
           Created: 05/20/2019
           Description:
                List all active project names and their ID's
        """
        all_project_items = list(TSC.Pager(server.projects, self.req_option))
        ##all_project_items, pagination_item = server.projects.get()
        project_names = [proj.name for proj in all_project_items]
        project_ids = [proj.id for proj in all_project_items]
        return [project_names, project_ids]

    def list_workbooks(self, server):
        """
            Created: 05/28/2019
            Description:
                List workbook ID's from a specific Project
        """
        all_workbooks = list(TSC.Pager(server.workbooks, self.req_option))
        ##all_workbooks, pagination_items = server.workbooks.get()
        workbook_names = [work.name for work in all_workbooks]
        workbook_ids = [work.id for work in all_workbooks]
        return [workbook_names, workbook_ids]

    def publish_datasource(self, server, source_path, project_id):
        """
            Created: 04/25/2019
            Description:
                Publish/Overwrite Datasource to Tableau Server
        """
        ##THIS IS HAVING ISSUES.... Maybe update Tableau Server Client
        ## Publishing a hyper datasource completes but there seems to be an issue with the data on the server
        # Use the project id to create new datsource_item
        new_datasource = TSC.DatasourceItem(project_id)

        # publish data source (specified in file_path)
        new_datasource = server.datasources.publish(
                          new_datasource, source_path, 'Overwrite')

    def refresh_workbook(self, server, server_wrkbk_ids):
        """
            Created: 04/25/2019
            Description:
                Refresh a workbook
        """
        for wkbk in server_wrkbk_ids:
            server.workbooks.refresh(workbook_id=wkbk)

    def package_workbook(self, server, server_wrkbk_names, out_dir):
        """
           Created: 04/23/2019
           Description:
                Download Workbook(s) defined in SERVER_WRKBK_NAMES from the server
                Package them as TWBX and store them in the OUT_DIR
        """
        # Gets all Workbook items
        all_workbooks = list(TSC.Pager(server.workbooks, self.req_option))
        for workbook in all_workbooks:
            #Fetch the workbook ID's we need
            if workbook.name in server_wrkbk_names:
                print("Downloading {0} to {1}".format(str(workbook.id), out_dir))
                server.workbooks.download(workbook.id, filepath=out_dir)

"""
#Testing Commands
# Calls Methods to evaluate performance
#Local Environment Variables:
working_dir = r"\\bec-home\Tableau\DEV\NISC\NISC_CCB_DATA_SMARTSHEETS"
output_tdsx_directory = os.path.join(working_dir,"TDSX")
output_twbx_directory = r"J:\DEV\MemSvc\New Service Team\Open Orders"
output_hyper_directory = os.path.join(working_dir, "Data")

#Call the Method sending it hardplastic Encryption
tsm_method = bec_tsm_data_methods('amxpc3QwMDE=', 'QWRkRmllbGREZWxpbWluaXRlcnMxMiE=')

#Generate the Authorization Token
tableau_auth = tsm_method.tableau_auth()

#Use that Token to connect to the Server URL
server = tsm_method.server_sign_in(tableau_auth, 'http://tabdev')

#Here we want to publish a datasource to the server:
tsm_method.publish_datasource(
                                server,
                                r'\\BEC-HOME\Tableau\DEV\Sysops\Construction\Open Construction Jobs\Data\construction_jobs_open (bec_gis_Partner).hyper',
                                'be4e8126-0440-4a4e-95ad-cc508696e5ea'
                                )

#Here we want to refresh a workbook
tsm_method.refresh_workbook(server, ['a5cf0125-7604-442b-bbc5-e18ee43f79d3'])

#Here we want to fetch Datasources from the Tableau Server
# Note: Tableau doesn't allow preps to hook up to server datasources
#       BUT it seems like it is a planned feature
# So instead we download the TDSX versions of the published datasource
# and we extract the Hyper Datasource from there
'''
tsm_method.fetch_datasources(
                                server,
                                ['CCB Data Analysis Agenda', 'CCB Business Analysis Agenda'], #Make sure you List em
                                output_tdsx_directory
                                )
'''
#Here we want to fetch workbooks from the Tableau Server and Package them as TWBX
##tsm_method.package_workbook(server,['New Service'],output_twbx_directory)

# We downloaded the TDSX files... but that doesn't help us because the data is contained in them
# SO we unpackage the Hyper datasets so we can use them in our Tableau Flow!
##unpack_tdsx(output_tdsx_directory, output_hyper_directory)
#Make sure to sign out from the server when you are done
tsm_method.server_sign_out(server)
del tsm_method

#So we know we have a shit load of projects and their IDs and often we need a specifc ID
# The following illustrates how to generate a list of the projects and their respective ID's
from bec_tableau.bec_tsm import *
import itertools

#Call the Method sending it hardplastic Encryption
tsm_method = bec_tsm_data_methods('amxpc3QwMDE=', 'UHlweW9kYmMxMiE=')

#Generate the Authorization Token
tableau_auth = tsm_method.tableau_auth()

#Use that Token to connect to the Server URL
server = tsm_method.server_sign_in(tableau_auth, 'http://tabdev')

projects = tsm_method.list_projects(server)

for x, y in zip(projects[0], projects[1]):
    print x, y
"""

