import tkinter as tk
from tkinter import ttk as ttk


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        queryFrame = self.queryFrame = tk.Frame(master, bd=10, bg="black")
        queryFrame.config(relief="sunken")
        queryFrame.config(cursor="pirate")
        queryFrame.pack(pady=10, anchor="center")

        queryLabel = self.queryLabel = tk.Label(queryFrame, text="SQl Query: ")
        queryLabel.grid(row=0, column=0, padx=10, pady=10)

        queryEntry = self.queryEntry = tk.Entry(queryFrame, width=100)
        queryEntry.grid(row=0, column=1, padx=10)

        queryButton = self.queryButton = tk.Button(queryFrame, text="Consultar")
        queryButton.grid(row=0, column=2, padx=10)

        # ----------------------------Results of the search----------------------------

        resultFrame = self.resultFrame = tk.Frame(master, bd=10)
        resultFrame.config(relief="sunken")
        resultFrame.pack(pady=2, anchor="center")

        resultTree = self.treeview = ttk.Treeview(resultFrame)
        resultTree.grid(row=0, column=0)


root = tk.Tk()
myapp = App(root)
myapp.master.minsize(800, 400)
myapp.master.title("Execution Plan window")
myapp.mainloop()
