# MileStone4

## Database Installation Setup 

Run the quickInstallDatabase.py for quick install.<br/>

    Note: You will need to download the 'AISTestData_dump.mysql' file<br/>
    and place it in the 'data/sql' directory.

OR, install the database manually:

1. Creating the database and the tables:<br/>
Move to the 'data/sql' directory and run the following commands in powershell or bash.
    >Windows<br/>
    \> Get-Content AISTestDataCreateTables.mysql | mysql -u \<user> -p --password=\<password>
    
    >Mac<br/>
    >$ mysql -u \<user> -p --password=\<password> < AISTestDataCreateTables.mysql

2. Populating the database:<br/>
Download the 'AISTestData_dump.mysql' (not found in this repository), and move it to the 'data/sql' directory.
Or just download and move to the directory wherever you saved the file, and then run the following command in powershell or bash.
    >Windows<br/>
    \> Get-Content AISTestData_dump.mysql | mysql -u \<user> -p --password=\<password>
    
    >MAC<br/>
    $ mysql -u \<user> -p --password=\<password> < AISTestData_dump.mysql
    Download the AISTestData_dump.mysql




















