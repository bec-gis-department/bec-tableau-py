#-------------------------------------------------------------------------------
# Name:        John gets it
# Purpose:
#
# Author:      Jlist001
#
# Created:     13/12/2018
# Copyright:   (c) uaserver 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import base64

def softplastic(in_string):
    """softplastic is fantastic"""
    return base64.decodestring(in_string)

def hardplastic(in_string):
    """hard plastic turns into softplastic"""
    return base64.encodestring(in_string)