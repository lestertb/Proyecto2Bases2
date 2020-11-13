import tkinter
from tkinter import messagebox, ttk
import pyodbc
from tkinter import *


# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port


def connexion(server, database, username, password):
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return cnxn


# cursor = cnxn.cursor()
# cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'pais'")
# for row in cursor:
#   print(row)

def main():
    root = Tk()
    root.geometry("800x600")
    root.title("Segundo Proyecto bases 2")
    e = Entry(root, width=50)
    e.grid(column=3, columnspan=3, padx=10, pady=10)
    e.insert(0, "LESTERTB\SQLEXPRESS")
    e2 = Entry(root, width=50)
    e2.grid(row=1, column=3, columnspan=3, padx=10, pady=10)
    e2.insert(0, "test_DB")
    e3 = Entry(root, width=50)
    e3.grid(row=2, column=3, columnspan=3, padx=10, pady=10)
    e3.insert(0, "ClaseDB")
    e4 = Entry(root, width=50)
    e4.grid(row=3, column=3, columnspan=3, padx=10, pady=10)
    e4.insert(0, "1234")
    servers = Entry.get(e)
    databases = Entry.get(e2)
    usernames = Entry.get(e3)
    passwords = Entry.get(e4)

    def mycclick():
        server = servers
        database = databases
        username = usernames
        password = passwords
        try:
            conn = connexion(server, database, username, password)
            tkinter.messagebox.showinfo(title="Exito", message="Conectado con exito")
            root.destroy()
            ventanaDespues(conn)
            conn.close()
        except pyodbc.Error as err:
            tkinter.messagebox.showerror(title="Error", message=err)
            root.destroy()
            main()

    boton = Button(root, text="Probar conexion", command=mycclick)
    boton.grid(row=4, column=3)
    root.mainloop()


def ventanaDespues(conn):
    # Globals
    newroot = Tk()
    newroot.geometry("800x600")
    newroot.title("Segundo Proyecto bases 2")


    nombreVariable = Text(newroot)
    nombreVariable.config(width=25, height=10, padx=25, pady=15)
    nombreVariable.place(x=50, y=100)  # ubicacion en x y y

    def getSchemas():
        cur = conn.cursor()
        # cur.execute("SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES where TABLE_TYPE = 'BASE TABLE'")
        cur.execute("SELECT DISTINCT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA ")
        data = []
        for tabla_list in cur.fetchall():
            data.append(tabla_list[0])
        return data


    label = Label(newroot, text="Seleccione el esquema al cual pertenece la tabla")
    label.grid(row=1, column=0)
    comboBoxSchemas = ttk.Combobox(newroot, width="20", values= getSchemas())
    comboBoxSchemas.place(x=25, y=25)
    comboBoxTables = ttk.Combobox(newroot, width=40)

    def callback(eventObject):
        comboBoxTables.set('')
        resultado()

    comboBoxSchemas.bind("<<ComboboxSelected>>", callback)

    def resultado():
        if comboBoxSchemas.get() != '':
            nombreVariable.delete('1.0', END)
            comboBoxTables["values"] = llenarComboBoxTablas(comboBoxSchemas.get())
            comboBoxTables.place(x=200, y=70)
            privilegiosTabla(comboBoxTables.get())
        else:
            tkinter.messagebox.showinfo(title="Advertencia", message="Debe elegir un schema")

    def llenarComboBoxTablas(valSchema):
        cur = conn.cursor()
        cur.execute(
            '''SELECT DISTINCT [TABLE_NAME] FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = ? and TABLE_TYPE = 'BASE TABLE' ''',valSchema)
        data = []
        for val in cur.fetchall():
            data.append(val[0])
        return data


    def privilegiosTabla(valTable):
        if valTable != '':
            testString = "sp_table_privileges "+ valTable
            cur = conn.cursor()
            rows = cur.execute(testString).fetchall()
            nombreVariable.insert(END, rows)
        else:
            tkinter.messagebox.showinfo(title="Advertencia", message="Debe elegir una tabla")


    boton1 = Button(newroot, text="Ver privilegios de la tabla", command=resultado)
    boton1.grid(row=4, column=3)

    newroot.mainloop()


main()
