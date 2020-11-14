import pyodbc


def get_connection(server, database, username, password):
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server +
                                    ';DATABASE=' + database +
                                    ';UID=' + username +
                                    ';PWD=' + password)
        return connection
    except pyodbc.Error as err:
        return None
