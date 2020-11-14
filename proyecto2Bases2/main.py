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
    labelConexion = Label(root, text="Conexion a la base de datos")
    labelConexion.place(x=200, y=15)
    labelConexion.config(font=("Courier", 14))
    e = Entry(root, width=25)
    e.place(x=300, y=50)
    e.insert(0, "MARCO\SQLEXPRESS")
    labelServidor = Label(root, text="Nombre del servidor")
    labelServidor.place(x=125, y=50)

    e2 = Entry(root, width=25)
    e2.place(x=300, y=90)
    e2.insert(0, "coronavirus")
    labelBD = Label(root, text="Nombre de la base de datos")
    labelBD.place(x=125, y=90)

    e3 = Entry(root, width=25)
    e3.place(x=300, y=130)
    e3.insert(0, "ClaseDB")

    labelUser = Label(root, text="Nombre de usuario")
    labelUser.place(x=125, y=130)

    e4 = Entry(root, width=25)
    e4.place(x=300, y=170)
    e4.insert(0, "12345")
    labelContra = Label(root, text="Contraseña")
    labelContra.place(x=125, y=170)

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
    boton.place(x=300, y=210)
    root.mainloop()


def ventanaDespues(conn):
    # Globals
    newroot = Tk()
    newroot.geometry("1500x800")
    newroot.title("Segundo Proyecto bases 2")
    labelMonitor = Label(newroot, text="Monitor de privilegios")
    labelMonitor.place(x=150, y=20)
    labelMonitor.config(width=50)
    labelMonitor.config(font=("Courier", 24))
    textoCentral = Text(newroot)
    textoCentral.config(width=120, height=30, padx=25, pady=15)
    textoCentral.place(x=50, y=150)  # ubicacion en x y y

    def getSchemas():
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA ")
        data = []
        for tabla_list in cur.fetchall():
            data.append(tabla_list[0])
        return data

    label = Label(newroot, text="Seleccione el esquema al cual pertenece la tabla")
    label.place(x=50, y=60)
    comboBoxSchemas = ttk.Combobox(newroot, width="20", values=getSchemas())
    comboBoxSchemas.place(x=50, y=95)
    comboBoxTables = ttk.Combobox(newroot, width=40)
    comboBoxAttributes = ttk.Combobox(newroot, width=40)

    def callback(eventObject):
        comboBoxTables.set('')
        resultado()

    def callback2(eventObject):
        comboBoxAttributes.set('')
        llenarComboBoxAtributos()

    comboBoxSchemas.bind("<<ComboboxSelected>>", callback)
    comboBoxTables.bind("<<ComboboxSelected>>", callback2)
    def resultado():
        if comboBoxSchemas.get() != '':
            textoCentral.delete('1.0', END)
            comboBoxTables["values"] = llenarComboBoxTablas(comboBoxSchemas.get())
            comboBoxTables.place(x=1200, y=150)
            labelTablas = Label(newroot, text="Seleccione la tabla con la que quiere trabajar")
            labelTablas.place(x=1200, y=125)
            privilegiosTabla(comboBoxTables.get())

        else:
            tkinter.messagebox.showinfo(title="Advertencia", message="Debe elegir un schema")

    def llenarComboBoxTablas(valSchema):
        cur = conn.cursor()
        cur.execute(
            '''SELECT DISTINCT [TABLE_NAME] FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = ? and TABLE_TYPE = 'BASE TABLE' ''',
            valSchema)
        data = []
        for val in cur.fetchall():
            data.append(val[0])
        return data

    def privilegiosTabla(valTable):
        if valTable != '':
            testString = "sp_table_privileges " + valTable
            cur = conn.cursor()
            cur.execute(testString)
            for rows in cur:
                info = "TABLE_QUALIFER" + " " + rows[0] + " " + "TABLE_NAME" + " " + rows[2] + " " + \
                       "Privilige" + " " + rows[5]
                info += '\n'
                info += '\n'
                textoCentral.insert(END, info)
            # labelAtributos = Label(newroot, text="Seleccione el atributo con el que quiere trabajar")
            # labelAtributos.place(x=1200, y=230)
            # comboBoxAttributes["values"] = llenarComboAtributos(valTable)
            # comboBoxAttributes.place(x=1200, y=250)
        else:
            tkinter.messagebox.showinfo(title="Advertencia", message="Debe elegir una tabla")

    def llenarComboAtributos(tabla):
        cur = conn.cursor()
        cur.execute(
            '''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ? ''',
            tabla)
        data = []
        for val in cur.fetchall():
            data.append(val[0])
        return data

    def atributosTabla():
        if comboBoxTables.get() != '' and comboBoxAttributes.get() != '':
            textoCentral.delete('1.0', END)
            verAtributosText(comboBoxTables.get(), comboBoxAttributes.get())
        else:
            tkinter.messagebox.showinfo(title="Advertencia", message="Debe elegir una tabla y un atributo")

    def verAtributosText(valTable, column):
        if valTable != '' and column != '':
            string = "sp_column_privileges " + valTable + " ,NULL " + " ,NULL " + ',' + column
            cur = conn.cursor()
            cur.execute(string)
            for rows in cur:
                string1 = "TABLE_QUALIFER =" + " " + rows[0] + " - " + "TABLE_NAME =" + " " + rows[2] + " - " \
                          + "COLUMN_NAME =" + " " + rows[3] + " - " + \
                          "Privilige =" + " " + rows[6]
                string1 += '\n'
                string1 += '\n'
                textoCentral.insert(END, string1)

        else:
            tkinter.messagebox.showinfo(title="Advertencia", message="Debe elegir una tabla y un atributo")

    def llenarComboBoxAtributos():

        labelAtributos = Label(newroot, text="Seleccione el atributo con el que quiere trabajar")
        labelAtributos.place(x=1200, y=230)
        comboBoxAttributes["values"] = llenarComboAtributos(comboBoxTables.get())
        comboBoxAttributes.place(x=1200, y=250)

    boton1 = Button(newroot, text="Ver privilegios de la tabla", command=resultado)
    boton1.place(x=1200, y=180)
    boton2 = Button(newroot, text="Ver privilegios de los atributos en la tabla seleccionada", command=atributosTabla)
    boton2.place(x=1200, y=280)

    newroot.mainloop()


main()
