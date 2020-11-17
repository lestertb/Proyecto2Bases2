import tkinter as tk
from tkinter import ttk,messagebox
import pyodbc
import xmltodict
import json
import os
def execution_plan(conn):
    root = tk.Tk()
    root.minsize(800, 400)
    root.title("Execution Plan window")
    style = ttk.Style()
    style.theme_use('clam')

    queryFrame = tk.Frame(root, bd=10, bg="black")
    queryFrame.config(cursor="pirate")
    queryFrame.pack(pady=10, anchor="center")

    cLabel = tk.Label(queryFrame, text="Tipo de reporte: ",font='Courier 12')
    cLabel.grid(row=0, column=0, padx=10, pady=10)
    comboBoxTypes = ttk.Combobox(queryFrame, width="20", values=["Detallado/Estimado","Detallado/Actual","Simple"],justify='center',font='Courier 12')
    comboBoxTypes.grid(row=0, column=1, padx=10, pady=10)
    comboBoxTypes.current(0)

    queryLabel = tk.Label(queryFrame, text="SQl Query: ",font='Courier 12')
    queryLabel.grid(row=1, column=0, padx=10, pady=10)

    queryEntry = tk.Text(queryFrame)
    queryEntry.config(width=120, height=5, padx=25, pady=15)
    queryEntry.grid(row=1, column=1, padx=10)

    scrollb = ttk.Scrollbar(queryFrame, command=queryEntry.yview)
    scrollb.grid(row=1, column=2, sticky='nsew')
    queryEntry['yscrollcommand'] = scrollb.set

    resultFrame = tk.Frame(root, bd=10)
    resultFrame.config(relief="sunken")
    resultFrame.pack(pady=2, anchor="center")

    resultTree = ttk.Treeview(resultFrame)
    resultTree.grid(row=0, column=0)

    def executeConsult():
        query = queryEntry.get("1.0", 'end-1c')
        queryConfig = ""

        print(comboBoxTypes.current())
        if (comboBoxTypes.current() == 0):
            queryConfig = "SET SHOWPLAN_XML ON"
            queryConfig1 = "SET STATISTICS XML OFF"
            queryConfig2 = "SET SHOWPLAN_ALL OFF"
        elif(comboBoxTypes.current() == 1):
            queryConfig = "SET STATISTICS XML ON"
            queryConfig1 = "SET SHOWPLAN_XML OFF"
            queryConfig2 = "SET SHOWPLAN_ALL OFF"
        else:
            queryConfig = "SET SHOWPLAN_ALL ON"
            queryConfig1 = "SET STATISTICS XML OFF"
            queryConfig2 = "SET SHOWPLAN_XML OFF"

        try:

            res = conn.cursor()
            res.execute(queryConfig1)
            res.execute(queryConfig2)
            res.execute(queryConfig)
            res.execute(query)
            xmlHelper = ""

            if (comboBoxTypes.current() == 0):
                resultSet = res.fetchone()
                xmlHelper = '<root>' + resultSet[0] + '</root>'
            elif (comboBoxTypes.current() == 1):
                res.nextset()
                resultSet = res.fetchone()
                xmlHelper = '<root>' + resultSet[0] + '</root>'



            json_convert = ""
            if(comboBoxTypes.current()<2):
                dictionary = xmltodict.parse(xmlHelper)
                json_convert = json.dumps(dictionary)
            if (comboBoxTypes.current() == 2):
                dictionary = res.fetchall()
                acc = []
                for x in dictionary:
                    split = x[0].split(",")
                    for e in split:
                        acc.append(e)
                print(acc)
                json_convert = json.dumps(acc)
                print(acc)
            file = open(r"treeView.json", "wt")
            file.write(json_convert)
            file.close()
            os.system("python3 json_viewer.py treeView.json")
            return json_convert

        except pyodbc.Error as err:
            tk.messagebox.showerror(title="Error", message=err)

    queryButton = tk.Button(queryFrame, text="Consultar",command = executeConsult,font='Courier 12')
    queryButton.grid(row=1, column=3, padx=10)

    # ----------------------------Results of the search----------------------------


    root.mainloop()

