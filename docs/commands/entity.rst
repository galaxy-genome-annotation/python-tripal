entity
======

This section is auto-generated from the help text for the tripaille command
``entity``.


``add_entity`` command
----------------------

**Usage**::

    tripaille entity add_entity [OPTIONS] ENTITY

**Help**

Add a new entity to the database


**Output**


    Entity information
    
**Options**::


      --params TEXT  Values to populate the entity fields
      -h, --help     Show this message and exit.
    

``get_entities`` command
------------------------

**Usage**::

    tripaille entity get_entities [OPTIONS]

**Help**

Get entities


**Output**


    Entity information
    
**Options**::


      --entity TEXT        Name of the entity type (e.g. Organism)
      --entity_id INTEGER  ID of an entity
      -h, --help           Show this message and exit.
    

``get_fields`` command
----------------------

**Usage**::

    tripaille entity get_fields [OPTIONS] ENTITY

**Help**

Get the list of available fields for an entity


**Output**


    Fields information
    
**Options**::


      -h, --help  Show this message and exit.
    
