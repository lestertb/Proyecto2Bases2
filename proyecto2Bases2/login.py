#Selected GUI libs to build graphical interface
import tkinter
#messagebox is typical of this library
from tkinter import messagebox
#This library was chosen because the wide information that is spread in internet, its
#very popular between developers.It serves to make connections to differents database engines
import pyodbc
from tkinter import *
from menu import menu


#This function creates the login window for the project
def main():
    root = Tk()
    root.geometry("600x800")
    root.title("Segundo Proyecto bases 2")

    canvas = Canvas(root, width=400, height=200)
    canvas.pack(anchor="center")
    img = PhotoImage(file="resources/logo-tec.png")
    canvas.create_image(210, 140, anchor="center", image=img)


    labelConexion = Label(root, text="Conexion a la base de datos",font='Courier 14 bold')
    labelConexion.pack(pady=10, anchor="center")


    labelServidor = Label(root, text="Direccion del servidor",font='Courier 12')
    labelServidor.pack(pady=10, anchor="center")

    e = Entry(root, width=25,justify='center',font='Courier 12')
    e.pack(pady=10, anchor="center")

    labelBD = Label(root, text="Nombre de la base de datos",font='Courier 12')
    labelBD.pack(pady=10, anchor="center")

    e2 = Entry(root, width=25,justify='center',font='Courier 12')
    e2.pack(pady=10, anchor="center")

    labelUser = Label(root, text="Nombre de usuario",font='Courier 12')
    labelUser.pack(pady=10, anchor="center")

    e3 = Entry(root, width=25,justify='center',font='Courier 12')
    e3.pack(pady=10, anchor="center")

    labelContra = Label(root, text="Contraseña",font='Courier 12')
    labelContra.pack(pady=10, anchor="center")

    e4 = Entry(root, width=25,justify='center',show = "*",font='Courier 12')
    e4.pack(pady=10, anchor="center")



#This function makes the connection to the database using Pyodbc
    def connexion(server, database, username, password):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        return conn
#Function to go to the selection menu
    def myclick():
        if e.get() != '' or e2.get() != '' or e3.get() != '' or e4.get() != '':
            try:
                conn = connexion(e.get(), e2.get(), e3.get(), e4.get())
                if conn:
                    tkinter.messagebox.showinfo(title="Exito", message="Conectado con exito")
                    root.destroy()
                    menu.menu(conn)


                else:
                    tkinter.messagebox.showinfo(title="Error", message="No conectado")


            except pyodbc.Error as err:
                tkinter.messagebox.showerror(title="Error", message=err)
                print(err)
                root.destroy()
                main()

        else:
            tkinter.messagebox.showerror(title="Advertencia", message="Campos vacios")
#Exit the application
    def salir():
        root.destroy()



    boton = Button(root, text="Iniciar sesion", font='Courier 12' ,command=myclick)
    boton.pack(pady=10, anchor="center")

    botonSalir = Button(root, text="Salir del programa",font='Courier 12', command=salir)
    botonSalir.pack(pady=10, anchor="center")

    root.mainloop()

if __name__ == '__main__':
    main()