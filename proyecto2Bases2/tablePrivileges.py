import tkinter
from tkinter import messagebox, ttk
import pyodbc
from tkinter import *
from proyecto2Bases2 import menu

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port



# cursor = cnxn.cursor()
# cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'pais'")
# for row in cursor:
#   print(row)

def tablePrivileges(conn):
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
        try:
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA ")
            data = []
            for tabla_list in cur.fetchall():
                data.append(tabla_list[0])
            return data
        except pyodbc.Error as err:
            tkinter.messagebox.showerror(title="Error", message=err)

    label = Label(newroot, text="Seleccione el esquema al cual pertenece la tabla")
    label.place(x=50, y=60)
    comboBoxSchemas = ttk.Combobox(newroot, width="20", values=getSchemas())
    comboBoxSchemas.place(x=50, y=95)
    comboBoxTables = ttk.Combobox(newroot, width=40)
    comboBoxAttributes = ttk.Combobox(newroot, width=40)

    def callback(eventObject):
        try:
            comboBoxTables.set('')
            resultado()
        except RuntimeError as err:
            tkinter.messagebox.showerror(title="Error", message=err)

    def callback2(eventObject):
        try:
            comboBoxAttributes.set('')
            llenarComboBoxAtributos()
        except RuntimeError as err:
            tkinter.messagebox.showerror(title="Error", message=err)

    comboBoxSchemas.bind("<<ComboboxSelected>>", callback)
    comboBoxTables.bind("<<ComboboxSelected>>", callback2)

    def resultado():
        try:
            if comboBoxSchemas.get() != '':
                textoCentral.delete('1.0', END)
                comboBoxTables["values"] = llenarComboBoxTablas(comboBoxSchemas.get())
                comboBoxTables.place(x=1200, y=150)
                labelTablas = Label(newroot, text="Seleccione la tabla con la que quiere trabajar")
                labelTablas.place(x=1200, y=125)
                privilegiosTabla(comboBoxTables.get())
            else:
                tkinter.messagebox.showinfo(title="Advertencia", message="Debe elegir un schema")
        except AttributeError as err:
            tkinter.messagebox.showerror(title="Error", message=err)

    def llenarComboBoxTablas(valSchema):
        try:
            cur = conn.cursor()
            cur.execute(
                '''SELECT  DISTINCT [TABLE_NAME] FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = ? and TABLE_TYPE = 'BASE TABLE' ''',
                valSchema)
            data = []
            for val in cur.fetchall():
                data.append(val[0])
            return data
        except pyodbc.Error as err:
            tkinter.messagebox.showerror(title="Error", message=err)

    def privilegiosTabla(valTable):
        if valTable != '':
            try:
                testString = "sp_table_privileges " + valTable
                cur = conn.cursor()
                cur.execute(testString)
                for rows in cur:
                    info = "TABLE_QUALIFER" + " " + rows[0] + " " + "TABLE_NAME" + " " + rows[2] + " " + \
                           "Privilige" + " " + rows[5]
                    info += '\n'
                    info += '\n'
                    textoCentral.insert(END, info)
            except pyodbc.Error as err:
                tkinter.messagebox.showerror(title="Error", message=err)
        else:
            tkinter.messagebox.showinfo(title="Advertencia", message="Debe elegir una tabla")

    def llenarComboAtributos(tabla):
        try:
            cur = conn.cursor()
            cur.execute(
                '''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ? ''',
                tabla)
            data = []
            for val in cur.fetchall():
                data.append(val[0])
            return data
        except pyodbc.Error as err:
            tkinter.messagebox.showerror(title="Error", message=err)

    def atributosTabla():
        try:
            if comboBoxTables.get() != '' and comboBoxAttributes.get() != '':
                textoCentral.delete('1.0', END)
                verAtributosText(comboBoxTables.get(), comboBoxAttributes.get())
            else:
                tkinter.messagebox.showinfo(title="Advertencia", message="Debe elegir una tabla y un atributo")
        except AttributeError as err:
            tkinter.messagebox.showerror(title="Error", message=err)

    def verAtributosText(valTable, column):
        if valTable != '' and column != '':
            try:
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
            except pyodbc.Error as err:
                tkinter.messagebox.showerror(title="Error", message=err)
        else:
            tkinter.messagebox.showinfo(title="Advertencia", message="Debe elegir una tabla y un atributo")

    def llenarComboBoxAtributos():
        try:
            labelAtributos = Label(newroot, text="Seleccione el atributo con el que quiere trabajar")
            labelAtributos.place(x=1200, y=230)
            comboBoxAttributes["values"] = llenarComboAtributos(comboBoxTables.get())
            comboBoxAttributes.place(x=1200, y=250)
        except AttributeError as err:
            tkinter.messagebox.showerror(title="Error", message=err)

    boton1 = Button(newroot, text="Ver privilegios de la tabla", command=resultado)
    boton1.place(x=1200, y=180)
    boton2 = Button(newroot, text="Ver privilegios de los atributos en la tabla seleccionada", command=atributosTabla)
    boton2.place(x=1200, y=280)


    newroot.mainloop()

