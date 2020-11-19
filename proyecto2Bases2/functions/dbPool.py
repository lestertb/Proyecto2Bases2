import pyodbc
#This library was chosen because the wide information that is spread in internet, its
#very popular between developers.It serves to make connections to differents database engines

#This function makes the connection to a SQL SERVER database
def get_connection(server, database, username, password):
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server +
                                    ';DATABASE=' + database +
                                    ';UID=' + username +
                                    ';PWD=' + password)
        return connection
    except pyodbc.Error as err:
        return None

