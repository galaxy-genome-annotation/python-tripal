feature
=======

This section is auto-generated from the help text for the tripaille command
``feature``.


``delete_orphans`` command
--------------------------

**Usage**::

    tripaille feature delete_orphans [OPTIONS]

**Help**

Delete orphans Drupal feature nodes


**Output**


    status
    
**Options**::


      --job_name TEXT  Name of the job
      --no_wait        Return immediately without waiting for job completion
      -h, --help       Show this message and exit.
    

``get_features_tripal`` command
-------------------------------

**Usage**::

    tripaille feature get_features_tripal [OPTIONS]

**Help**

Get features entities


**Output**


    Feature entity/node information
    
**Options**::


      --feature_id INTEGER  A feature entity/node ID
      -h, --help            Show this message and exit.
    

``sync`` command
----------------

**Usage**::

    tripaille feature sync [OPTIONS]

**Help**

Synchronize some features


**Output**


    status
    
**Options**::


      --organism TEXT     Common name of the organism to sync
      --organism_id TEXT  ID of the organism to sync
      --max_sync TEXT     Maximum number of features to sync (default: all)
      --types TEXT        List of types of records to be synced (e.g. gene mRNA,
                          default: all)
      --ids TEXT          List of names of records to be synced (e.g. gene0001,
                          default: all)
      --job_name TEXT     Name of the job
      --no_wait           Return immediately without waiting for job completion
      -h, --help          Show this message and exit.
    
