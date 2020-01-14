#-------------------------------------------------------------------------------
# Name:        Example Hyper Creation from GDB
# Purpose:     Generate Hyper Extract from Feature Class
#               Can be used in 64 bit geoprocessing
#
# Author:      J Lister - GIS Applications Developer
#
# Created:     14/01/2020
# Copyright:   (c) uaserver 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# bec_tableau 1st to prevent the ctypes error [143]
from bec_tableau.bec_hyper import * #Hyper Generation

#set arcpy environment to the gdb
arcpy.env.workspace = 'gdb path'

#1) Conductor Extract Generation
conductor_mileage_fdr = 'feature class'
conductor_hyper = os.path.join(prod_tableau_dir, 'outHyper.hyper')
build_hyper_esri(conductor_mileage_fdr, conductor_hyper, 'Hyper Table')