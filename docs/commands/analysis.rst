analysis
========

This section is auto-generated from the help text for the tripaille command
``analysis``.


``add_analysis`` command
------------------------

**Usage**::

    tripaille analysis add_analysis [OPTIONS] NAME PROGRAM PROGRAMVERSION

**Help**

Create an analysis


**Output**


    Analysis information
    
**Options**::


      --algorithm TEXT      analysis algorithm
      --sourceversion TEXT  analysis sourceversion
      --sourceuri TEXT      analysis sourceuri
      --description TEXT    analysis description
      --date_executed TEXT  analysis date_executed (yyyy-mm-dd)
      -h, --help            Show this message and exit.
    

``get_analyses`` command
------------------------

**Usage**::

    tripaille analysis get_analyses [OPTIONS]

**Help**

Get analyses


**Output**


    Analysis information
    
**Options**::


      --analysis_id TEXT     An analysis ID
      --name TEXT            analysis name
      --program TEXT         analysis program
      --programversion TEXT  analysis programversion
      --algorithm TEXT       analysis algorithm
      --sourcename TEXT      analysis sourcename
      --sourceversion TEXT   analysis sourceversion
      --sourceuri TEXT       analysis sourceuri
      --date_executed TEXT   analysis date_executed (yyyy-mm-dd)
      -h, --help             Show this message and exit.
    

``get_analysis_nodes`` command
------------------------------

**Usage**::

    tripaille analysis get_analysis_nodes [OPTIONS]

**Help**

Get analysis nodes


**Output**


    Analysis node information
    
**Options**::


      --node INTEGER  filter on node id
      -h, --help      Show this message and exit.
    

``load_blast`` command
----------------------

**Usage**::

    tripaille analysis load_blast [OPTIONS] NAME PROGRAM PROGRAMVERSION

**Help**

Create a Blast analysis


**Output**


    Loading information
    
**Options**::


      --blast_ext TEXT         If looking for files in a directory, extension of the
                               blast result files
      --blastdb TEXT           Name of the database blasted against (must be in the
                               Chado db table)
      --blastdb_id TEXT        ID of the database blasted against (must be in the
                               Chado db table)
      --blast_parameters TEXT  Blast parameters used to produce these results
      --query_re TEXT          The regular expression that can uniquely identify the
                               query name. This parameters is required if the
                               feature name is not the first word in the blast query
                               name.
      --query_type TEXT        The feature type (e.g. 'gene', 'mRNA', 'contig') of
                               the query. It must be a valid Sequence Ontology term.
      --query_uniquename       Use this if the --query-re regular expression matches
                               unique names instead of names in the database.
      --is_concat              If the blast result file is simply a list of
                               concatenated blast results.
      --search_keywords        Extract keywords for Tripal search
      --no_wait                Do not wait for job to complete
      --algorithm TEXT         analysis algorithm
      --sourceversion TEXT     analysis sourceversion
      --sourceuri TEXT         analysis sourceuri
      --description TEXT       analysis description
      --date_executed TEXT     analysis date_executed (yyyy-mm-dd)
      -h, --help               Show this message and exit.
    

``load_fasta`` command
----------------------

**Usage**::

    tripaille analysis load_fasta [OPTIONS] FASTA

**Help**

Load fasta sequences


**Output**


    Loading information
    
**Options**::


      --organism TEXT          Organism common name or abbreviation
      --organism_id INTEGER    Organism ID
      --analysis TEXT          Analysis name
      --analysis_id INTEGER    Analysis ID
      --sequence_type TEXT     Sequence type  [default: contig]
      --re_name TEXT           Regular expression for the name
      --re_uniquename TEXT     Regular expression for the unique name
      --db_ext_id TEXT         External DB ID
      --re_accession TEXT      Regular expression for the accession from external DB
      --rel_type TEXT          Relation type (part_of or derives_from)
      --rel_subject_re TEXT    Relation subject regular expression (used to extract
                               id of related entity)
      --rel_subject_type TEXT  Relation subject type (must match already loaded
                               data, e.g. mRNA)
      --method TEXT            Insertion method (insert, update or insup,
                               default=insup (Insert and Update))  [default: insup]
      --match_type TEXT        Match type for already loaded features (name or
                               uniquename; default=uniquename; used for "Update
                               only" or "Insert and update" methods)'  [default:
                               uniquename]
      --job_name TEXT          Name of the job
      --no_wait                Do not wait for job to complete
      -h, --help               Show this message and exit.
    

``load_gff3`` command
---------------------

**Usage**::

    tripaille analysis load_gff3 [OPTIONS] GFF

**Help**

Load GFF3 file


**Output**


    Loading information
    
**Options**::


      --organism TEXT               Organism common name or abbreviation
      --organism_id INTEGER         Organism ID
      --analysis TEXT               Analysis name
      --analysis_id INTEGER         Analysis ID
      --import_mode TEXT            Import mode (add_only=existing features won't be
                                    touched, update=existing features will be
                                    updated and obsolete attributes kept,
                                    refresh=existing features will be updated and
                                    obsolete attributes removed, remove=features
                                    present in the db and in the GFF3 file will be
                                    removed)')  [default: update]
      --target_organism TEXT        In case of Target attribute in the GFF3, choose
                                    the organism abbreviation or common name to
                                    which target sequences belong. Select this only
                                    if target sequences belong to a different
                                    organism than the one specified with --organism-
                                    id. And only choose an organism here if all of
                                    the target sequences belong to the same species.
                                    If the targets in the GFF file belong to
                                    multiple different species then the organism
                                    must be specified using the
                                    'target_organism=genus:species' attribute in the
                                    GFF file.')
      --target_organism_id INTEGER  In case of Target attribute in the GFF3, choose
                                    the organism ID to which target sequences
                                    belong. Select this only if target sequences
                                    belong to a different organism than the one
                                    specified with --organism-id. And only choose an
                                    organism here if all of the target sequences
                                    belong to the same species. If the targets in
                                    the GFF file belong to multiple different
                                    species then the organism must be specified
                                    using the 'target_organism=genus:species'
                                    attribute in the GFF file.')
      --target_type TEXT            In case of Target attribute in the GFF3, if the
                                    unique name for a target sequence is not unique
                                    (e.g. a protein and an mRNA have the same name)
                                    then you must specify the type for all targets
                                    in the GFF file. If the targets are of different
                                    types then the type must be specified using the
                                    'target_type=type' attribute in the GFF file.
                                    This must be a valid Sequence Ontology (SO)
                                    term.')
      --target_create               In case of Target attribute in the GFF3, if the
                                    target feature cannot be found, create one using
                                    the organism and type specified above, or using
                                    the 'target_organism' and 'target_type' fields
                                    specified in the GFF file. Values specified in
                                    the GFF file take precedence over those
                                    specified above.')
      --start_line INTEGER          The line in the GFF file where importing should
                                    start
      --landmark_type TEXT          A Sequence Ontology type for the landmark
                                    sequences in the GFF fie (e.g. 'chromosome').
      --alt_id_attr TEXT            When ID attribute is absent, specify which other
                                    attribute can uniquely identify the feature.
      --create_organism             Create organisms when encountering organism
                                    attribute (these lines will be skip otherwise)
      --re_mrna TEXT                Regular expression for the mRNA name
      --re_protein TEXT             Replacement string for the protein name
      --job_name TEXT               Name of the job
      --no_wait                     Do not wait for job to complete
      -h, --help                    Show this message and exit.
    

``load_go`` command
-------------------

**Usage**::

    tripaille analysis load_go [OPTIONS] NAME PROGRAM PROGRAMVERSION

**Help**

Create a GO analysis


**Output**


    Loading information
    
**Options**::


      --gaf_ext TEXT        If looking for files in a directory, extension of the
                            GAF files
      --query_type TEXT     The feature type (e.g. 'gene', 'mRNA', 'contig') of the
                            query. It must be a valid Sequence Ontology term.
      --query_uniquename    Use this if the --query-re regular expression matches
                            unique names instead of names in the database.
      --method TEXT         Import method ('add' or 'remove')  [default: add]
      --re_name TEXT        Regular expression to extract the feature name from GAF
                            file.
      --no_wait             Do not wait for job to complete
      --algorithm TEXT      analysis algorithm
      --sourceversion TEXT  analysis sourceversion
      --sourceuri TEXT      analysis sourceuri
      --description TEXT    analysis description
      --date_executed TEXT  analysis date_executed (yyyy-mm-dd)
      -h, --help            Show this message and exit.
    

``load_interpro`` command
-------------------------

**Usage**::

    tripaille analysis load_interpro [OPTIONS] NAME PROGRAM PROGRAMVERSION

**Help**

Create an Interpro analysis


**Output**


    Loading information
    
**Options**::


      --interpro_parameters TEXT  InterProScan parameters used to produce these
                                  results
      --query_re TEXT             The regular expression that can uniquely identify
                                  the query name. This parameters is required if the
                                  feature name is not the first word in the blast
                                  query name.
      --query_type TEXT           The feature type (e.g. 'gene', 'mRNA', 'contig')
                                  of the query. It must be a valid Sequence Ontology
                                  term.
      --query_uniquename          Use this if the query_re regular expression
                                  matches unique names instead of names in the
                                  database.
      --parse_go                  Load GO annotation to the database
      --no_wait                   Do not wait for job to complete
      --algorithm TEXT            analysis algorithm
      --sourceversion TEXT        analysis sourceversion
      --sourceuri TEXT            analysis sourceuri
      --description TEXT          analysis description
      --date_executed TEXT        analysis date_executed (yyyy-mm-dd)
      -h, --help                  Show this message and exit.
    

``sync`` command
----------------

**Usage**::

    tripaille analysis sync [OPTIONS]

**Help**

Synchronize an analysis


**Output**


    status
    
**Options**::


      --analysis TEXT     Analysis name
      --analysis_id TEXT  ID of the analysis to sync
      --job_name TEXT     Name of the job
      --no_wait           Return immediately without waiting for job completion
      -h, --help          Show this message and exit.
    
