"""
<<BEC Tableau Module Library>>

Author:
    John Lister - GIS Applications Developer
    Email: john.lister@bluebonnet.coop
Purpose:
    House modules that specifically work with Tableau

Modules:
    -twbx_update (10/10/2018) John Lister - GIS Applications Developer
    -bec_hyper (11/19/2018) John Lister - GIS Applications Developer
    -bec_tsm (04/25/2019) John Lister - GIS Applications Developer
    -general_functions (04/25/2019) John Lister - GIS Applications Developer
    -tdsx_unpack (03/22/2019) John Lister - GIS Applications Developer

<<Module Descriptions>>

    <twbx_update>

        Purpose:
            Update a Packaged Tableau Work Book with new data
            Replicates TWBX zip folder structure in Directory located in same Directory as TWBX
            Rezips the Generated Structure into the TWBX with the new datasource

        Functions:
            __init__:
                Initialize the Class object with the following parameters
                    Input:
                        self - Bound variable or Object
                        twbx_file - Input Real String path to the destination TWBX
                    Set:
                        self.structure_dir - Build the Location of the Structure Drive from the Input TWBX
                        self.data_dir - Set the Data Directory within the Structure
                        self.twbx_file - Set the twbx file from the input

            map_twbx:
                Replicate TWBX structure in self.struct_dir
                    Input:
                        self
                    Return:
                        N/A

            move_shp:
                Moves all components of ESRI Shapefiles using Arcpy Copy Features
                Moves SHP to self.data_dir
                    Input:
                        self
                        in_shp -  input Real Path to input Shapefile
                    Return:
                        N/A

            move_data:
                Move Single File to self.data_dir
                Used for files with only 1 component EG .hyper, .xls, . tde
                    Input:
                        self
                        in_data: Real Path to Input Data
                    Returns:
                        N/A

            repackage_twbx:
                Rebuild the TWBX from the contents in the Structure Directory
                    Input:
                        self
                    Returns:
                        N/A

        Code Sample:

            (1) Useage with single .xls update file
                twbx_obj = twbxUpdate(twbx_file) #Build the Object
                twbx_obj.map_twbx() #Map the TWBX in the Structure Dir
                twbx_obj.move_data(out_xls) #Move a .xls to the Data Dir
                twbx_obj.repackage_twbx() #Rebuild the TWBX with the new Data

            (2) Useage with .shp update file
                twbx_obj = twbxUpdate(twbx_file) #Build the Object
                twbx_obj.map_twbx() #Map the TWBX in the Structure Dir
                twbx_obj.move_shp(out_shp)  #Move a .shp to the Data Dir
                twbx_obj.repackage_twbx() #Rebuild the TWBX with the new Data

    <<bec_hyper.py>>

        Purpose:
            Generate a Hyper extract using the Tableau Extract API 2.0 for Python (64bit)
            Conversion Methods are defined to convert datatypes from the input to the .hyper extract
            Recommended practice is to overwrite the existing extract [JOHN MAYBE FIND WAY TO TRUNCATE IT]

        Current Methods:
            esri_type:
                __init__
                    Initialize the method with the following Parameters:
                        Input:
                            In Data (Input ESRI Dataset)
                            Out Extract (The initialized extract object
                            hyper_name (String input to tell the Hyper engine what name it needs to give the hyper table)
                        Set:
                            self.in_names - derive field names from input dataset
                            self.in_types - derive esri datatypes from input dataset
                            self.out_table_name - set the extracts table name [PERHAPS DERIVE IT FROM THE SYSTEM JOHN]

                define_columns:
                    Set the Hyper Extract Schema to match the input data
                    Parameters:
                        Self
                    Return:
                        Return [LIST of Successfull column names], [LIST of Successfull column Types]]

                define_rows:
                    Set build row objects for the hyper extract from input rows
                    Defines insert method based on input datatype
                    Parameters:
                        [LIST] of [Successfull column names], and [Successfull column Types]
                    Returns:
                        N/A

        Code Sample:
            (1) Generate Extract from ESRI Datatype input
                import os
                from tableausdk import *
                from tableausdk.HyperExtract import *
                from bec_tableau.bec_hyper import * #This is module

                in_data = r'path to in data' #ESRI File Type in
                out_hyper = r'path to destination.hyper' #Can exist or could be new

                # Initialize the Tableau Extract API
                ExtractAPI.initialize()

                #Remove the Existing Extract
                if os.path.exists(out_hyper):
                  os.remove(out_hyper)

                #Build the Extract
                demo_extract = Extract(out_hyper)

                #Fun stuff here
                # Call the ESRI Type Method
                hyper_obj = esri_type(in_data, demo_extract)

                names_n_types = hyper_obj.define_columns()

                hyper_obj.define_rows(names_n_types)

                del hyper_obj

                # Flush the Extract to Disk
                demo_extract.close()

                # Close the Tableau Extract API
                ExtractAPI.cleanup()

    <<tdsx_unpack.py>>

        Purpose:
            Generate a Hyper extract using the Tableau Extract API 2.0 for Python (64bit)
            Conversion Methods are defined to convert datatypes from the input to the .hyper extract
            Recommended practice is to overwrite the existing extract [JOHN MAYBE FIND WAY TO TRUNCATE IT]

        Current Methods:
            tdsx_unpack:
                __init__
                    Initialize the method with the following Parameters:
                        Input:
                            tdsx_file (Input path to TDSX File to unpack)
                            Out Extract (The initialized extract object
                            hyper_name (String input to tell the Hyper engine what name it needs to give the hyper table)
                        Set:
                            self.in_names - derive field names from input dataset
                            self.in_types - derive esri datatypes from input dataset
                            self.out_table_name - set the extracts table name [PERHAPS DERIVE IT FROM THE SYSTEM JOHN]

                define_columns:
                    Set the Hyper Extract Schema to match the input data
                    Parameters:
                        Self
                    Return:
                        Return [LIST of Successfull column names], [LIST of Successfull column Types]]

                define_rows:
                    Set build row objects for the hyper extract from input rows
                    Defines insert method based on input datatype
                    Parameters:
                        [LIST] of [Successfull column names], and [Successfull column Types]
                    Returns:
                        N/A

        Code Sample:
            (1) Generate Extract from ESRI Datatype input
                import os
                from tableausdk import *
                from tableausdk.HyperExtract import *
                from bec_tableau.bec_hyper import * #This is module

                in_data = r'path to in data' #ESRI File Type in
                out_hyper = r'path to destination.hyper' #Can exist or could be new

                # Initialize the Tableau Extract API
                ExtractAPI.initialize()

                #Remove the Existing Extract
                if os.path.exists(out_hyper):
                  os.remove(out_hyper)

                #Build the Extract
                demo_extract = Extract(out_hyper)

                #Fun stuff here
                # Call the ESRI Type Method
                hyper_obj = esri_type(in_data, demo_extract)

                names_n_types = hyper_obj.define_columns()

                hyper_obj.define_rows(names_n_types)

                del hyper_obj

                # Flush the Extract to Disk
                demo_extract.close()

                # Close the Tableau Extract API
                ExtractAPI.cleanup()

    <<bec_tsm.py>>

        Purpose:
            Generate a Hyper extract using the Tableau Extract API 2.0 for Python (64bit)
            Conversion Methods are defined to convert datatypes from the input to the .hyper extract
            Recommended practice is to overwrite the existing extract [JOHN MAYBE FIND WAY TO TRUNCATE IT]

        Current Methods:
            tdsx_unpack:
                __init__
                    Initialize the method with the following Parameters:
                        Input:
                            tdsx_file (Input path to TDSX File to unpack)
                            Out Extract (The initialized extract object
                            hyper_name (String input to tell the Hyper engine what name it needs to give the hyper table)
                        Set:
                            self.in_names - derive field names from input dataset
                            self.in_types - derive esri datatypes from input dataset
                            self.out_table_name - set the extracts table name [PERHAPS DERIVE IT FROM THE SYSTEM JOHN]

                define_columns:
                    Set the Hyper Extract Schema to match the input data
                    Parameters:
                        Self
                    Return:
                        Return [LIST of Successfull column names], [LIST of Successfull column Types]]

                define_rows:
                    Set build row objects for the hyper extract from input rows
                    Defines insert method based on input datatype
                    Parameters:
                        [LIST] of [Successfull column names], and [Successfull column Types]
                    Returns:
                        N/A

        Code Sample:
            (1) Generate Extract from ESRI Datatype input
                import os
                from tableausdk import *
                from tableausdk.HyperExtract import *
                from bec_tableau.bec_hyper import * #This is module

                in_data = r'path to in data' #ESRI File Type in
                out_hyper = r'path to destination.hyper' #Can exist or could be new

                # Initialize the Tableau Extract API
                ExtractAPI.initialize()

                #Remove the Existing Extract
                if os.path.exists(out_hyper):
                  os.remove(out_hyper)

                #Build the Extract
                demo_extract = Extract(out_hyper)

                #Fun stuff here
                # Call the ESRI Type Method
                hyper_obj = esri_type(in_data, demo_extract)

                names_n_types = hyper_obj.define_columns()

                hyper_obj.define_rows(names_n_types)

                del hyper_obj

                # Flush the Extract to Disk
                demo_extract.close()

                # Close the Tableau Extract API
                ExtractAPI.cleanup()
"""