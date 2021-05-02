from data.python.mysqlutils import MySQLConnectionManager
import mysql.connector, configparser


def setUp():
    """
    Function for the setting up a small small sample database

    :return:
    """
    con = None
    cfg = '../sql/connection_data.conf'
    config = configparser.ConfigParser()
    success = config.read(cfg)
    if not success:
        raise configparser.Error("Could not read file {}".format(cfg))

    try:
        con = mysql.connector.connect(user=config['SQL']['user'], password=config['SQL']['password'],
                                      host=config['SQL']['host'])
        cursor = con.cursor()
        with open('../sql/AISTestDataCreateTables.mysql', 'r') as file:
            query = file.read()
            for result in cursor.execute(query, multi=True):
                if result.with_rows:
                    result.fetchall()

    except Exception as e:
        print(e)
    finally:
        con.close()


if __name__ == '__main__':
    setUp()
























