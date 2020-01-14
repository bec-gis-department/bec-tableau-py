#-------------------------------------------------------------------------------
# Name:        BEC Tableau hyper Construction
# Purpose:     Builds a Hyper Extract from an input datasource
#
# Author:      J Lister - GIS Applications Developer
#
# Created:     16/11/2018
# Copyright:   (c) jlist001 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Import Modules
# THE TABLEAU SDK NEEDS TO IMPORTED 1st.... K
from tableausdk import *
from tableausdk.HyperExtract import *
#--------------------------------------------
import os
import sys
import datetime
import arcpy
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#------------------------Define Extract Columns and Rows------------------------

# We need to define rules for assigning datatypes in the Hyper Extract
# These Rules are used to determine the Column Schema and Insert Row DataTypes

# 1) ESRI Geodatabase Data Types (.mdb Tables/Features, .gdb Tables/Features, .shp Files)
class esri_type:
    def __init__(self, in_table, out_extract, hyper_name):
        self.in_data = in_table
        self.in_names = [f.name for f in arcpy.ListFields(in_table)]
        self.in_types = [f.type for f in arcpy.ListFields(in_table)]
        self.out_extract = out_extract
        self.out_table_name = hyper_name

    def define_columns(self):
        """Define the Hyper Data Type for input ESRI Field Object"""

        #Build Insert Column Info
        # This could possibly be a redundancy but I think its smart for right meow
        # We need to read the data but surely we only care about the data that successully matches the extract schema?
        # YES So we are going to build a list of ESRI Types/Names that were successfull
        # The List of Successful field names will be used in the data search cursor and the Types to derive the method
        success_names = []
        success_types = []

        #Handle Input Field Object
        in_names = self.in_names
        in_types = self.in_types

        #Make the __init__ variables prettier
        out_schema = TableDefinition()
        out_table = self.out_table_name
        extract = self.out_extract

        #Iterate and Build Columns to Extract Schema
        for i in range(len(in_types)):
            in_type = in_types[i]
            in_name = in_names[i]
            #Text Types
            if in_type == "String" or in_type == "Guid":
                out_schema.addColumn(in_names[i], Type.UNICODE_STRING) # Don't forgot about Type.CHAR_STRING... if it ever throws problems
                success_names.append(in_name)
                success_types.append(in_type)
            #Date Types
            elif in_type == "Datetime":
                out_schema.addColumn(in_names[i], Type.DATETIME)
                success_names.append(in_name)
                success_types.append(in_type)
            elif in_type == "Date":
                out_schema.addColumn(in_names[i], Type.DATE)
                success_names.append(in_name)
                success_types.append(in_type)
            #Numeric Types
            elif in_type == "float" or in_type == "Double":
                out_schema.addColumn(in_names[i], Type.DOUBLE)
                success_names.append(in_name)
                success_types.append(in_type)
            elif in_type == "Integer" or in_type == "SmallInteger":
                out_schema.addColumn(in_names[i], Type.INTEGER)
                success_names.append(in_name)
                success_types.append(in_type)
            #True False (BOOLEAN) I dont think ESRI cares
            ##Type.BOOLEAN
        #Set the Schema
        # If it fails we kill it
        out_table = extract.addTable(out_table, out_schema)
        if (out_table == None ):
            print('A fatal error occurred while creating the table:\nExiting now\n.')
            sys.exit()

        #Pass this result to the define rows function as this tells it what it needs
        return [success_names, success_types]

    def define_rows(self, names_n_types):
        """Build the Insert Rows using ESRI Search Cursor and Tableau Hyper Extract"""

        #Make the input easier to use
        search_fields = names_n_types[0]
        print(search_fields)
        insert_types = names_n_types[1] # Note this is still in ESRI we need to define the Hyper type in the row (row.setString())

        # use our search fields to get some rows
        search_cursor = arcpy.da.SearchCursor(self.in_data, search_fields)

        # Make the __init__ variables prettier
        out_table = self.out_table_name
        extract = self.out_extract

        # Get the Schema of the Table we built in define_columns
        table = extract.openTable(out_table)
        insert_schema = table.getTableDefinition()

        #Set Row object
        row = Row(insert_schema)

        #The Fun Part, don't get lost...
        # Iterate the Rows from the input
        for in_row in search_cursor:
            # Iterate the cells and datatypes using i
            for i in range(len(in_row)):
                cell = in_row[i]
                in_type = insert_types[i]
                # For some Reason Tableau doesn't like None's... so I guess lets NULL it?
                if cell is None:
                    row.setNull(i)
                else:
                    #Define the Hyper Cell DataTypes
                    #Text
                    if in_type == "String" or in_type == "Guid":
                        row.setString(i, str(cell.encode('ascii',errors='ignore'))) ##Added s.encode('ascii',errors='ignore') to account for ASCII, str(cell) is the og
                    #Numeric Types
                    elif in_type == "Float" or in_type == "Double":
                        row.setDouble(i, cell)
                    elif in_type == "Integer" or in_type == "SmallInteger":
                        row.setInteger(i, cell)
                    #Date Types...needs a bit of logic
                    elif in_type == "Date":
                        year_ = cell.year
                        month_ = cell.month
                        day_ = cell.day
                        row.setDate(i, year_, month_, day_)
                    elif in_type == "Datetime":
                        year_ = cell.year
                        month_ = cell.month
                        day_ = cell.day
                        hour_ = cell.hour
                        minute_ = cell.minute
                        # I don't care for seconds and fraction of a second but we can change this if need be
                        second_ = 0
                        frac_ = 0
                        row.setDate(i, year_, month_, day_, hour_, minute_, second_, frac_)
            #Commit the row
            table.insert(row)
        del search_cursor
        #Close extract to drop lock
        extract.close()
#-------------------------------------------------------------------------------
#2) Smartsheet Table Type
# This is used to only if the smartsheet data is destined straight for the .hyper extract
# EG. Osmose writes to a geodatabase so it doesn't need this it would use 1) ESRI Geodatabase

#-------------------------------------------------------------------------------
#3) Pypyodbc Type
# This is used to interpret row tuples derived from a pypyodbc connection
# Data types from Python types returned by Pypyodbc (https://github.com/mkleehammer/pyodbc/wiki/Data-Types) are mapped to Tableau Extract
class pypyodbc_type:
    def __init__(self, in_rows, in_fields, in_field_types, out_extract, hyper_name):
        """Initialize function receives [List] of rows, [List] of field names, [List] of field types, Hyper Extract OBJECT, and a STR Hyper Table Name"""
        self.in_rows = in_rows # Tuple of Rows
        self.in_fields = in_fields # Associated fields
        self.in_field_types = in_field_types
        self.out_extract = out_extract #Hyper Extract Object
        self.out_table_name = hyper_name #String input defining what name we are giving the Hyper Extract Table

    def define_columns(self):
        """Used to derive the columns for the Hyper Extract from the input columns"""
        #Build Insert Column Info
        #Handle Input Field Object
        in_names = self.in_fields
        in_types = self.in_field_types

        #Make the __init__ variables prettier
        out_schema = TableDefinition()
        out_table = self.out_table_name
        extract = self.out_extract

        #Iterate and Build Columns to Extract Schema
        for i in range(len(in_types)):
            in_type = in_types[i]
            in_name = in_names[i]
            #Text Types
            if in_type == 'str':
                out_schema.addColumn(in_names[i], Type.UNICODE_STRING) # Don't forgot about Type.CHAR_STRING... if it ever throws problems
            #Date Types
            elif in_type == 'datetime.datetime':
                out_schema.addColumn(in_names[i], Type.DATETIME)
            elif in_type == 'datetime.date':
                out_schema.addColumn(in_names[i], Type.DATE)
            ## Figure out a match for time if needed... may just need to use datetime but they do have Type.DURATION?
            #Numeric Types
            elif in_type == 'float':
                out_schema.addColumn(in_names[i], Type.DOUBLE)
            elif in_type == "int":
                out_schema.addColumn(in_names[i], Type.INTEGER)
                #T?F
            elif in_type == 'bool':
                out_schema.addColumn(in_names[i], Type.BOOLEAN)
        #Set the Schema
        # If it fails we kill it
        out_table = extract.addTable(out_table, out_schema)
        if (out_table == None ):
            print('A fatal error occurred while creating the table:\nExiting now\n.')
            sys.exit()

    def define_rows(self):
        """Build the Insert Rows using ESRI Search Cursor and Tableau Hyper Extract"""

        # Make the __init__ variables prettier
        in_rows = self.in_rows
        in_types = self.in_field_types
        extract = self.out_extract
        out_table = self.out_table_name

        # Get the Schema of the Table we built in define_columns
        table = extract.openTable(out_table)
        insert_schema = table.getTableDefinition()

        #Set Row object
        row = Row(insert_schema)

        #The Fun Part, don't get lost...
        # Iterate the Rows from the input
        for in_row in in_rows:
            # Iterate the cells and datatypes using i
            for i in range(len(in_row)):
                cell = in_row[i]
                in_type = in_types[i]
                # For some Reason Tableau doesn't like None's... so I guess lets NULL it
                if cell is None:
                    ##pass
                    # I donno, setNull was having a freakout with column index 18 TableauException: TableauException (303): invalid column number
                    row.setNull(i)
                else:
                    #Define the Hyper Cell DataTypes
                    #Text
                    if in_type == 'str':
                        row.setString(i, cell)
                    #Numeric Types
                    elif in_type == 'float':
                        row.setDouble(i, cell)
                    elif in_type == 'int':
                        row.setInteger(i, cell)
                    #T/F
                    elif in_type == 'bool':
                        row.setBoolean(i, cell)
                    #Date Types...needs a bit of logic
                    elif in_type == "datetime.date":
                        year_ = cell.year
                        month_ = cell.month
                        day_ = cell.day
                        row.setDate(i, year_, month_, day_)
                    elif in_type == "datetime.datetime":
                        year_ = cell.year
                        month_ = cell.month
                        day_ = cell.day
                        hour_ = cell.hour
                        minute_ = cell.minute
                        # I don't care for seconds and fraction of a second but we can change this if need be
                        second_ = 0
                        frac_ = 0
                        row.setDate(i, year_, month_, day_, hour_, minute_, second_, frac_)
            #Commit the row
            table.insert(row)
        #Close extract to drop lock
        extract.close()
