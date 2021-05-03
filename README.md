# Milestone 4

## Database Installation

### Quick Installation

    1. You will need to download the 'AISTestData_dump.mysql' file and place it in the 'data/sql' directory.

    2. Run the 'quickInstallDatabase.py' for quick install.   

### Manual Installation

    1. Creating the database and the tables:
    Move to the 'data/sql' directory and run the following commands in powershell or bash.
   **Windows**
   
    \> Get-Content AISTestDataCreateTables.mysql | mysql -u \<user> -p --password=\<password>

   **Mac**
   
    >$ mysql -u \<user> -p --password=\<password> < AISTestDataCreateTables.mysql

    2. Populating the database:<br/>
    Download the 'AISTestData_dump.mysql' (not found in this repository), and move it to the 'data/sql' directory.
    Or just download and move to the directory wherever you saved the file, and then run the following command in powershell or bash.
   **Windows**
   
    \> Get-Content AISTestData_dump.mysql | mysql -u \<user> -p --password=\<password>

   **Mac**
   
    $ mysql -u \<user> -p --password=\<password> < AISTestData_dump.mysql

**Trouble Shooting**

- Be sure to use the provided AISTestData_dump.sql file


## Testing

    1. Navigate to 'milestone4/data/python' folder

    2. Run the 'testDAO.py'

    3. The testDAO.py will reinitialize the database before testing, but DOES NOT reinitialize after the completion of tests.

    (It is recommended that you reinitialize the database before executing individual functions to ensure you have an unaltered data set.)

**Trouble Shooting**

- Ensure database was installed correctly
- Ensure AISTestData_dump.sql is in the sql folder
- Ensure python is up-to-date
- Ensure the mysql-connector-python V 8.0.23 package is installed

### Interface Tests

    All functions have passing interface tests.

### Integration Tests

Tests for these functions are created but assert pass only.
- read_all_ship_positions_from_tile_scale3
- read_all_ship_positions_to_port
- read_all_ships_headed_to_port

## Additional Documentation 

You can find more detailed descriptions of the Function and their DocStrings [here]().
