expression
==========

This section is auto-generated from the help text for the tripaille command
``expression``.


``add_biomaterial`` command
---------------------------

**Usage**::

    tripaille expression add_biomaterial [OPTIONS] ORGANISM_ID FILE_PATH

**Help**

Add a new biomaterial to the database


**Output**


    Job information
    
**Options**::


      --no_wait   Do not wait for job to complete
      -h, --help  Show this message and exit.
    

``add_expression`` command
--------------------------

**Usage**::

    tripaille expression add_expression [OPTIONS] ORGANISM_ID ANALYSIS_ID

**Help**

:type organism_id: str :param organism_id: Organism Id


**Output**


    Loading information
    
**Options**::


      --match_type TEXT            Match to features using either name or
                                   uniquename. Default to uniquename  [default:
                                   uniquename]
      --biomaterial_provider TEXT  The contact who provided the biomaterial.
                                   (optional, non functional in Tripal2)
      --array_design TEXT          The array design associated with this analysis.
                                   This is not required if the experimental data was
                                   gathered from next generation sequencing methods.
                                   (optional, non functional in Tripal2)
      --assay_id TEXT              The id of the assay associated with the
                                   experiment. (optional, non functional in Tripal2)
      --acquisition_id TEXT        The id of the acquisition associated with the
                                   experiment (optional, non functional in Tripal2)
      --quantification_id TEXT     The id of the quantification associated with the
                                   experiment (optional, non functional in Tripal2)
      --file_extension TEXT        File extension for the file(s) to be loaded into
                                   Chado. Do not include the ".". Not required for
                                   matrix files. (optional)
      --start_regex TEXT           A regular expression to describe the line that
                                   occurs before the start of the expression data.
                                   If the file has no header, this is not needed.
                                   (optional)
      --stop_regex TEXT            A regular expression to describe the line that
                                   occurs after the end of the expression data. If
                                   the file has no footer text, this is not needed.
                                   (optional)
      --use_column                 Set if the expression file is a column file
      --no_wait                    Do not wait for job to complete
      -h, --help                   Show this message and exit.
    

``delete_biomaterials`` command
-------------------------------

**Usage**::

    tripaille expression delete_biomaterials [OPTIONS]

**Help**

Delete some biomaterials


**Output**


    status
    
**Options**::


      --names TEXT        JSON list of biomaterial names to delete. (optional)
      --organism_id TEXT  Organism id from which to delete biomaterials (optional)
      --analysis_id TEXT  Analysis id from which to delete biomaterials (optional)
      --job_name TEXT     Name of the job (optional)
      --no_wait           Return immediately without waiting for job completion
      -h, --help          Show this message and exit.
    

``get_biomaterials`` command
----------------------------

**Usage**::

    tripaille expression get_biomaterials [OPTIONS]

**Help**

List biomaterials in the database


**Output**


    Job information
    
**Options**::


      --provider_id TEXT     Limit query to the selected provider
      --biomaterial_id TEXT  Limit query to the selected biomaterial
      --organism_id TEXT     Limit query to the selected organism
      --dbxref_id TEXT       Limit query to the selected ref
      -h, --help             Show this message and exit.
    

``sync_biomaterials`` command
-----------------------------

**Usage**::

    tripaille expression sync_biomaterials [OPTIONS]

**Help**

Synchronize some biomaterials


**Output**


    status
    
**Options**::


      --ids TEXT       JSON list of ids of biomaterials to be synced (default: all)
      --max_sync TEXT  Maximum number of features to sync (default: all)
      --job_name TEXT  Name of the job
      --no_wait        Return immediately without waiting for job completion
      -h, --help       Show this message and exit.
    
