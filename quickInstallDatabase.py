import os

db_name = "AISTestData"
success_tables_msg = "\nInstallation for tables was successful.\n" \
              "Database Name: {}\n".format(db_name)
fail_msg = "\nUnsuccessful Install.\n" \
           "Use manual install method instead.\n"


def main():
    user, password = get_credentials()

    installer(user, password)
    print("Successfully finished installation.")


def installer(user, password):
    failure = True

    if os.name.lower() == 'nt':
        cmd_tables = r"type data\sql\AISTestDataCreateTables.mysql | mysql -u {} -p --password={}".format(user, password)
        cmd_populate = r"type data\sql\AISTestData_dump.mysql | mysql -u {} -p --password={}".format(user, password)
    elif os.name.lower() == 'posix':
        cmd_tables = None
        cmd_populate = None
    else:
        return failure

    failure = os.system(cmd_tables)
    if failure: return failure
    print(success_tables_msg)

    if permission_populate_tables():
        print("Populating tables. This may take a while...")
        failure = os.system(cmd_populate)
    if failure: return failure


def get_credentials():
    user = input("Quick Install> MySQL username: ")
    password = input("Quick Install> MySQL password: ")
    return user, password


def permission_populate_tables():
    answer = input("Quick Install> Would you like to also populate tables?\n"
                   "\t\t(This requires downloading the 'AISTestData_dump.mysql'\n"
                   "\t\tand moving the file to the root in 'data/sql') [y/n]").lower().strip()
    if answer in ['y', 'yes']:
        return True
    return False

if __name__ == '__main__':
    main()
