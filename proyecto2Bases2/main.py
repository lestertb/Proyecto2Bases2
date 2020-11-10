import logging
import tkinter
from tkinter import messagebox
import pyodbc
from tkinter import *

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port



def conneccion(server, database, username, password):
    cnxn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM pais")
    for row in cursor:
        print(row)
        row = cursor.fetchone()
        
def main():
    root = Tk()
    root.title("Segundo Proyecto bases 2")
    e = Entry(root, width=50)
    e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
    e.insert(0, "Server")
    e2 = Entry(root, width=50)
    e2.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    e2.insert(0, "Database")
    e3 = Entry(root, width=50)
    e3.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
    e3.insert(0, "Username")
    e4 = Entry(root, width=50)
    e4.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
    e4.insert(0, "Password")

    def mycclick():
        server = e.get()
        database = e2.get()
        username = e3.get()
        password = e4.get()
        try:
            conneccion(server, database, username, password)
        except pyodbc.Error as err:
            tkinter.messagebox.showerror(title="Error", message=err)
            root.destroy()
            main()

    myButton = Button(root, text='Probar conexion', command=mycclick)
    myButton.grid(row=4, column=0)
    root.mainloop()


main()
