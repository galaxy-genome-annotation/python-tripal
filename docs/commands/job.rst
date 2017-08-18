job
===

This section is auto-generated from the help text for the tripaille command
``job``.


``add_job`` command
-------------------

**Usage**::

    tripaille job add_job [OPTIONS] NAME MODULE CALLBACK ARGUMENTS

**Help**

Schedule a new job


**Output**


    Job information
    
**Options**::


      --priority INTEGER  An integer score to prioritize the job  [default: 10]
      -h, --help          Show this message and exit.
    

``get_jobs`` command
--------------------

**Usage**::

    tripaille job get_jobs [OPTIONS]

**Help**

Get all jobs


**Output**


    Jobs information
    
**Options**::


      --job_id INTEGER  job id
      -h, --help        Show this message and exit.
    

``get_logs`` command
--------------------

**Usage**::

    tripaille job get_logs [OPTIONS] STDOUT STDERR

**Help**

Get job output


**Output**


    Output information
    
**Options**::


      -h, --help  Show this message and exit.
    

``run_jobs`` command
--------------------

**Usage**::

    tripaille job run_jobs [OPTIONS]

**Help**

Run jobs in queue. There is no way to trigger a single job execution.


**Output**


    Job information
    
**Options**::


      --wait      Wait for job completion  [default: True]
      -h, --help  Show this message and exit.
    

``wait`` command
----------------

**Usage**::

    tripaille job wait [OPTIONS] JOB_ID

**Help**

Wait for a job completion


**Output**


    Job information
    
**Options**::


      -h, --help  Show this message and exit.
    
