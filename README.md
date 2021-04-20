# MileStone4

Installation setup (Windows):

Setup the Database: Get-Content AISTestDataCreateTables.mysql | mysql -u USER -p --password=PASSWORD

Download the AISTestData_dump.mysql

Populate the tables: Get-Content AISTestData_dump.mysql | mysql -u USER -p --password=PASSWORD

