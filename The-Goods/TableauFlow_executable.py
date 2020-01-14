#-------------------------------------------------------------------------------
# Name:        execute_flows (hourly)
# Purpose:     Execute Tableau Flows Hourly Every Weekday
#
# Author:      John R Lister - GIS Applications Developer
#
# Created:     26/06/2019
# Copyright:   (c) uaserver 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Standard Library
import subprocess
import itertools
import os

#Flow Executions
# 1) Contractor Budget Tracking
# Description: This flow executes J:\PROD\Sysops\Construction\Construction Contractor Budget Tracking\Library\2019constructionContractorBudget_Tracking.tfl
# Author: John R Lister
# Added: 01/13/2019
# Status: [PROD]
subprocess.call(r"Path to Batch File")

##You can just keep adding all the ones you want to execute here or just have them in the same batch file




