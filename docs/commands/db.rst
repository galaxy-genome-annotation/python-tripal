db
==

This section is auto-generated from the help text for the tripaille command
``db``.


``get_dbs`` command
-------------------

**Usage**::

    tripaille db get_dbs [OPTIONS]

**Help**

Get all dbs


**Output**


    Dbs information
    
**Options**::


      --db_id TEXT  A db ID
      --name TEXT   filter on db name
      -h, --help    Show this message and exit.
    

``get_mviews`` command
----------------------

**Usage**::

    tripaille db get_mviews [OPTIONS]

**Help**

Get all materialized views


**Output**


    materialized views information
    
**Options**::


      --name TEXT  filter on mview name
      -h, --help   Show this message and exit.
    

``index`` command
-----------------

**Usage**::

    tripaille db index [OPTIONS]

**Help**

Schedule database indexing using elasticsearch


**Output**


    Indexing information
    
**Options**::


      --mode TEXT        Indexing mode: 'website' to index everything, 'table' to
                         index a single table (default: website)  [default: website]
      --table TEXT       Table to index (only in 'table' mode)
      --index_name TEXT  Index name (only in 'table' mode)
      --queues INTEGER   Number of indexing task queues  [default: 10]
      --fields TEXT      Fields to index (only in 'table' mode), syntax:
                         <field_name>|<field_type>, field_type should be one of
                         'string', 'keyword', 'date', 'long', 'double', 'boolean',
                         'ip', 'object', 'nested', 'geo_point', 'geo_shape', or
                         'completion'
      --links TEXT       List of links to show to users, syntax: <column-where-to-
                         show-the-link>|</your/url/[any-column-name]>
      --tokenizer TEXT   Tokenizer to use (one of 'standard', 'letter', 'lowercase',
                         'whitespace', 'uax_url_email', 'classic', 'ngram',
                         'edge_ngram', 'keyword', 'pattern', or 'path_hierarchy';
                         default='standard')  [default: standard]
      --job_name TEXT    Name of the job
      --no_wait          Do not wait for job to complete
      -h, --help         Show this message and exit.
    

``populate_mviews`` command
---------------------------

**Usage**::

    tripaille db populate_mviews [OPTIONS]

**Help**

Populate materialized views


**Output**


    Loading information
    
**Options**::


      --name TEXT  filter on mview name
      --no_wait    Do not wait for job to complete
      -h, --help   Show this message and exit.
    
