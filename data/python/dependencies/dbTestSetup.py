import mysql.connector, configparser


def setUp():
    """
    Function for the setting up a small small sample database

    :return:
    """
    con = None
    cfg = r'..\sql\connection_data.conf'
    config = configparser.ConfigParser()
    success = config.read(cfg)
    if not success:
        raise configparser.Error("Could not read file {}".format(cfg))

    try:
        con = mysql.connector.connect(user=config['SQL']['user'], password=config['SQL']['password'],
                                      host=config['SQL']['host'])
        cursor = con.cursor()
        with open(r'..\sql\AISTestData_dump.mysql', 'r') as file:
            query = file.read()
            for result in cursor.execute(query, multi=True):
                if result.with_rows:
                    result.fetchall()
        con.commit()

    except Exception as e:
        print(e)
    finally:
        con.close()

























