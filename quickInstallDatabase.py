import os
from enum import Enum, auto


def main():
    Installer().run()


class OSType(Enum):
    WINDOWS = auto()
    POSIX = auto()
    NOT_FOUND = auto()


class Installer:
    db_name = "AISTestData"
    success_tables_msg = "\nInstallation for tables was successful.\n" \
                         "Database Name: {}\n".format(db_name)
    fail_msg = "\nUnsuccessful Install.\n" \
               "Use manual install method instead.\n"

    def __init__(self):
        self.os_type = self.get_os_type()
        self.mysql_username = None

    def run(self):
        self.mysql_username = self.get_username()
        cmd_create = self.get_create_table_cmd()
        cmd_populate = self.get_populate_table_cmd() if cmd_create else None

        failure = self.install(cmd_create, cmd_populate)
        if not failure:
            print("Successfully installed database.\n"
                  "Database Name: {}".format(Installer.db_name))
            return True
        return False

    def install(self, cmd_create, cmd_populate=None):
        failure = os.system(cmd_create)
        if failure:
            return failure
        print(self.success_tables_msg)

        if cmd_populate is not None:
            if self.permission_populate_tables():
                print("Enter mysql password for user <{}>.\nThis will populate tables and may take a while..."
                      .format(Installer.db_name))
                failure = os.system(cmd_populate)
                if failure:
                    return failure

        if cmd_populate is None:
            input("Could not locate 'data\\sql\\AISTestData_dump.mysql' file.\n"
                  "Please download the file and place in the above directory to populate tables. <enter>\n")

        return failure

    def get_username(self):
        user = input("Quick Install> MySQL username: ")
        return user

    def get_create_table_cmd(self):
        if not os.path.isfile("data/sql/AISTestDataCreateTables.mysql"):
            return None

        if self.os_type == OSType.WINDOWS:
            return r"type data\sql\AISTestDataCreateTables.mysql | mysql -u {} -p".format(self.mysql_username)
        elif self.os_type == OSType.POSIX:
            return r"cat data/sql/AISTestDataCreateTables.mysql | mysql -u {} -p".format(self.mysql_username)
        return None

    def get_populate_table_cmd(self):
        if not os.path.isfile("data/sql/AISTestData_dump.mysql"):
            return None

        if self.os_type == OSType.WINDOWS:
            return r"cat data\sql\AISTestData_dump.mysql | mysql -u {} -p".format(self.mysql_username)
        elif self.os_type == OSType.POSIX:
            return r"cat data/sql/AISTestData_dump.mysql | mysql -u {} -p".format(self.mysql_username)
        return None

    def permission_populate_tables(self):
        answer = input("Quick Install> Would you like to also populate tables?\n"
                       "\t\t(This requires downloading the 'AISTestData_dump.mysql'\n"
                       "\t\tand moving the file to the root in 'data/sql') [y/n]").lower().strip()
        if answer in ['y', 'yes']:
            return True
        return False

    def get_os_type(self):
        if os.name.lower() == 'nt':
            return OSType.WINDOWS
        elif os.name.lower() == 'posix':
            return OSType.POSIX
        return OSType.NOT_FOUND

if __name__ == '__main__':
    main()
