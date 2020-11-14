import tkinter
from tkinter import messagebox, ttk
import pyodbc
from tkinter import *
from proyecto2Bases2 import tablePrivileges

def connexion(server, database, username, password):
    try:
        cnxn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        return cnxn
    except pyodbc.Error as err:
        tkinter.messagebox.showerror(title="Error", message=err)

def main():
    root = Tk()
    root.geometry("600x800")
    root.title("Segundo Proyecto bases 2")

    canvas = Canvas(root, width=400, height=200)
    canvas.pack()
    img = PhotoImage(file="tec_logo.png")
    canvas.create_image(20, 20, anchor=CENTER, image=img)


    labelConexion = Label(root, text="Conexion a la base de datos")
    #labelConexion.place(x=200, y=15)
    labelConexion.pack(pady=10, anchor="center")

    labelConexion.config(font=("Courier", 14))
    e = Entry(root, width=25,justify='center')
    #e.place(x=300, y=50)
    e.pack(pady=10, anchor="center")
    e.insert(0, "MARCO\SQLEXPRESS")

    labelServidor = Label(root, text="Nombre del servidor")
    #labelServidor.place(x=125, y=50)
    labelServidor.pack(pady=10, anchor="center")

    e2 = Entry(root, width=25,justify='center')
    #e2.place(x=300, y=90)
    e2.pack(pady=10, anchor="center")
    e2.insert(0, "coronavirus")
    labelBD = Label(root, text="Nombre de la base de datos")
    #labelBD.place(x=125, y=90)
    labelBD.pack(pady=10, anchor="center")

    e3 = Entry(root, width=25,justify='center')
    #e3.place(x=300, y=130)
    e3.pack(pady=10, anchor="center")
    e3.insert(0, "ClaseDB")

    labelUser = Label(root, text="Nombre de usuario")
    #labelUser.place(x=125, y=130)
    labelUser.pack(pady=10, anchor="center")

    e4 = Entry(root, width=25,justify='center')
    #e4.place(x=300, y=170)
    e4.pack(pady=10, anchor="center")
    e4.insert(0, "12345")
    labelContra = Label(root, text="Contraseña")
    #labelContra.place(x=125, y=170)
    labelContra.pack(pady=10, anchor="center")

    server = Entry.get(e)
    database = Entry.get(e2)
    username = Entry.get(e3)
    password = Entry.get(e4)

    def mycclick():
        try:
            conn = connexion(server, database, username, password)
            tkinter.messagebox.showinfo(title="Exito", message="Conectado con exito")
            root.destroy()
            tablePrivileges.tablePrivileges(conn)
            conn.close()
        except pyodbc.Error as err:
            tkinter.messagebox.showerror(title="Error", message=err)
            root.destroy()
            main()

    boton = Button(root, text="Iniciar sesion", command=mycclick)
    #boton.place(x=300, y=210)
    boton.pack(pady=10, anchor="center")
    root.mainloop()

if __name__ == '__main__':
    main()